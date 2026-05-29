"""Application logging configuration."""

from __future__ import annotations

import logging
import os
from typing import Any, Callable

import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

CORRELATION_ID_HEADER = "X-Request-ID"


def _get_log_level() -> int:
	level_name = os.getenv("LOG_LEVEL", "INFO").upper()
	return logging._nameToLevel.get(level_name, logging.INFO)


def _use_json_logging() -> bool:
	log_format = os.getenv("LOG_FORMAT", "").lower()
	env = os.getenv("ENV", "").lower()
	return log_format == "json" or env in {"prod", "production", "staging"}


def _build_structlog_processors(use_json: bool) -> tuple[list[Callable[..., object]], list[Callable[..., object]], Callable[..., object]]:
	timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
	exception_processor = (
		structlog.processors.dict_tracebacks
		if use_json
		else structlog.processors.format_exc_info
	)

	def add_correlation_id(
		_: Any,
		__: str,
		event_dict: dict[str, Any],
	) -> dict[str, Any]:
		if "correlation_id" not in event_dict:
			cid = correlation_id.get()
			if cid:
				event_dict["correlation_id"] = cid
		return event_dict

	processors = [
		structlog.contextvars.merge_contextvars,  # merge bound contextvars into the event dict
		add_correlation_id,  # ensure correlation ID is present for all logs
		structlog.stdlib.add_logger_name,  # add logger name for routing/filters
		structlog.stdlib.add_log_level,  # add log level for readability
		timestamper,  # add ISO-8601 timestamp in UTC
		structlog.processors.StackInfoRenderer(),  # render stack when stack_info=True
		exception_processor,  # attach structured exception details
		structlog.processors.EventRenamer("message"),  # rename event key for common log ingestion
		structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # defer rendering to stdlib formatter
	]

	foreign_pre_chain = [
		structlog.contextvars.merge_contextvars,  # include request context for stdlib logs
		add_correlation_id,  # ensure correlation ID is present for stdlib logs
		structlog.stdlib.add_logger_name,  # keep logger name for non-structlog logs
		structlog.stdlib.add_log_level,  # include level for stdlib logs
		timestamper,  # add timestamps to stdlib logs
		structlog.processors.StackInfoRenderer(),  # render stack when stack_info=True
		exception_processor,  # attach structured exception details
		structlog.processors.EventRenamer("message"),  # unify message key
	]

	renderer = (
		structlog.processors.JSONRenderer()
		if use_json
		else structlog.dev.ConsoleRenderer()
	)

	return processors, foreign_pre_chain, renderer


def configure_logging() -> None:
	if getattr(configure_logging, "_configured", False):
		return

	use_json = _use_json_logging()
	processors, foreign_pre_chain, renderer = _build_structlog_processors(use_json)

	structlog.configure(
		processors=processors,
		context_class=dict,
		logger_factory=structlog.stdlib.LoggerFactory(),
		wrapper_class=structlog.stdlib.BoundLogger,
		cache_logger_on_first_use=True,
	)

	handler = logging.StreamHandler()
	handler.setFormatter(
		structlog.stdlib.ProcessorFormatter(
			processor=renderer,
			foreign_pre_chain=foreign_pre_chain,
		)
	)

	root_logger = logging.getLogger()
	root_logger.handlers = [handler]
	root_logger.setLevel(_get_log_level())

	for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
		logger = logging.getLogger(logger_name)
		logger.handlers.clear()
		logger.propagate = True
		logger.setLevel(root_logger.level)

	logging.captureWarnings(True)

	configure_logging._configured = True


async def bind_contextvars_middleware(
	request: Request,
	call_next: RequestResponseEndpoint,
) -> Response:
	cid = correlation_id.get()
	structlog.contextvars.clear_contextvars()
	if cid:
		structlog.contextvars.bind_contextvars(correlation_id=cid)

	try:
		response = await call_next(request)
		if cid:
			response.headers[CORRELATION_ID_HEADER] = cid
	except Exception:
		structlog.get_logger("app.error").exception("Unhandled exception")
		structlog.contextvars.clear_contextvars()
		raise
	else:
		response.call_on_close(structlog.contextvars.clear_contextvars)
		return response
