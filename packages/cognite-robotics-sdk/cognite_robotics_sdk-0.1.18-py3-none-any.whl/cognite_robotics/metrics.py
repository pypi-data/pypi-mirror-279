# -*- coding: utf-8 -*-
"""Prometheus metrics."""
import typing

import prometheus_client

METRICS_PORT = 8088


_registered_collectors: dict[str, prometheus_client.metrics.MetricWrapperBase] = {}


def setupRobotMetrics() -> None:
    """Set up Prometheus client and start metrics endpoint."""
    prometheus_client.start_http_server(METRICS_PORT)


def collectRobotMetrics() -> bytes:
    """Collect Prometheus metrics in text format."""
    return prometheus_client.generate_latest()


def getGaugeMetric(name: str) -> prometheus_client.Gauge:
    """Get a registered Gauge metric."""
    if name not in _registered_collectors:
        raise KeyError(f"{name} is not a registered collector")
    metric = _registered_collectors[name]
    if not isinstance(metric, prometheus_client.Gauge):
        raise ValueError(f"{name}[{type(metric)}] is registered but is not a Gauge metric")
    return metric


def getCounterMetric(name: str) -> prometheus_client.Counter:
    """Get a registered Counter metric."""
    if name not in _registered_collectors:
        raise KeyError(f"{name} is not a registered collector")
    metric = _registered_collectors[name]
    if not isinstance(metric, prometheus_client.Counter):
        raise ValueError(f"{name}[{type(metric)}] is registered but is not a Gauge metric")
    return metric


def getHistogramMetric(name: str) -> prometheus_client.Histogram:
    """Get a registered Histogram metric."""
    if name not in _registered_collectors:
        raise KeyError(f"{name} is not a registered collector")
    metric = _registered_collectors[name]
    if not isinstance(metric, prometheus_client.Histogram):
        raise ValueError(f"{name}[{type(metric)}] is registered but is not a Gauge metric")
    return metric


def createGauge(name: str, labels: typing.Iterable[str] = ()) -> prometheus_client.Gauge:
    """Create a Gauge metric."""
    metric = prometheus_client.Gauge(name, "", labelnames=labels)
    _registered_collectors[name] = metric
    return metric


def createCounter(name: str, labels: typing.Iterable[str] = ()) -> prometheus_client.Counter:
    """Create a Counter metric."""
    metric = prometheus_client.Counter(name, "", labelnames=labels)
    _registered_collectors[name] = metric
    return metric


def createHistogram(name: str, labels: typing.Iterable[str] = ()) -> prometheus_client.Histogram:
    """Create a Histogram metric."""
    metric = prometheus_client.Histogram(name, "", labelnames=labels)
    _registered_collectors[name] = metric
    return metric
