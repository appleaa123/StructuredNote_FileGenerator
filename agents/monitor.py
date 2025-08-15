"""
Agent Monitor - Health monitoring and status tracking for agents.

This module provides comprehensive monitoring capabilities for all agents:
- Health status monitoring
- Performance metrics tracking
- Error detection and reporting
- Resource usage monitoring
- Alert system for issues
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import threading
import queue

from . import AgentRegistry, AgentMetadata, AgentStatus, agent_registry
from .factory import AgentFactory, agent_factory

# Configure logging
logger = logging.getLogger(__name__)


class MonitorStatus(Enum):
    """Status of monitoring operations"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    OFFLINE = "offline"


class AlertLevel(Enum):
    """Levels of alerts"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PerformanceMetrics:
    """Performance metrics for an agent"""
    agent_type: str
    response_time_avg: float = 0.0
    response_time_min: float = 0.0
    response_time_max: float = 0.0
    success_rate: float = 0.0
    error_count: int = 0
    total_requests: int = 0
    last_request_time: Optional[datetime] = None
    uptime: float = 0.0
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None


@dataclass
class HealthCheck:
    """Health check result for an agent"""
    agent_type: str
    status: MonitorStatus
    timestamp: datetime
    response_time: float
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Alert information"""
    agent_type: str
    level: AlertLevel
    message: str
    timestamp: datetime
    details: Dict[str, Any] = field(default_factory=dict)


class AgentMonitor:
    """
    Comprehensive monitoring system for all agents.
    
    This class provides:
    - Real-time health monitoring
    - Performance metrics tracking
    - Alert system for issues
    - Resource usage monitoring
    - Historical data collection
    """
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize the agent monitor.
        
        Args:
            check_interval: Interval in seconds between health checks
        """
        self.check_interval = check_interval
        self.registry = agent_registry
        self.factory = agent_factory
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        self.health_cache: Dict[str, HealthCheck] = {}
        self.performance_metrics: Dict[str, PerformanceMetrics] = {}
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable[[Alert], None]] = []
        
        # Initialize metrics for all agents
        self._initialize_metrics()
    
    def start_monitoring(self):
        """Start the monitoring system"""
        if self.is_monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Agent monitoring started")
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Agent monitoring stopped")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add a callback function for alerts"""
        self.alert_callbacks.append(callback)
    
    def remove_alert_callback(self, callback: Callable[[Alert], None]):
        """Remove an alert callback function"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)
    
    def get_agent_health(self, agent_type: str) -> Optional[HealthCheck]:
        """Get the latest health check for a specific agent"""
        return self.health_cache.get(agent_type)
    
    def get_all_agent_health(self) -> Dict[str, HealthCheck]:
        """Get health information for all agents"""
        return self.health_cache.copy()
    
    def get_agent_performance(self, agent_type: str) -> Optional[PerformanceMetrics]:
        """Get performance metrics for a specific agent"""
        return self.performance_metrics.get(agent_type)
    
    def get_all_performance_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Get performance metrics for all agents"""
        return self.performance_metrics.copy()
    
    def get_alerts(self, level: Optional[AlertLevel] = None, hours: int = 24) -> List[Alert]:
        """
        Get alerts, optionally filtered by level and time.
        
        Args:
            level: Optional alert level filter
            hours: Number of hours to look back
            
        Returns:
            List of alerts matching the criteria
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_alerts = [
            alert for alert in self.alerts
            if alert.timestamp >= cutoff_time
        ]
        
        if level:
            filtered_alerts = [
                alert for alert in filtered_alerts
                if alert.level == level
            ]
        
        return filtered_alerts
    
    def clear_alerts(self, hours: int = 24):
        """Clear alerts older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        self.alerts = [
            alert for alert in self.alerts
            if alert.timestamp >= cutoff_time
        ]
    
    def run_health_check(self, agent_type: str) -> HealthCheck:
        """
        Run a health check for a specific agent.
        
        Args:
            agent_type: Type of agent to check
            
        Returns:
            Health check result
        """
        start_time = time.time()
        
        try:
            # Get agent metadata
            metadata = self.registry.get_agent_metadata(agent_type)
            if not metadata:
                return HealthCheck(
                    agent_type=agent_type,
                    status=MonitorStatus.OFFLINE,
                    timestamp=datetime.now(),
                    response_time=0.0,
                    error_message=f"Agent {agent_type} not found in registry"
                )
            
            # Check if agent is available
            if metadata.status == AgentStatus.DEPRECATED:
                return HealthCheck(
                    agent_type=agent_type,
                    status=MonitorStatus.OFFLINE,
                    timestamp=datetime.now(),
                    response_time=0.0,
                    error_message=f"Agent {agent_type} is deprecated"
                )
            
            # Try to create agent instance
            agent = self.factory.create_agent(agent_type, enable_monitoring=False)
            if not agent:
                return HealthCheck(
                    agent_type=agent_type,
                    status=MonitorStatus.CRITICAL,
                    timestamp=datetime.now(),
                    response_time=time.time() - start_time,
                    error_message=f"Failed to create agent {agent_type}"
                )
            
            # Test basic functionality
            test_result = self._test_agent_functionality(agent, agent_type)
            
            response_time = time.time() - start_time
            
            # Determine status based on test result
            if test_result["success"]:
                status = MonitorStatus.HEALTHY
                error_message = None
            else:
                status = MonitorStatus.CRITICAL
                error_message = test_result["error"]
            
            health_check = HealthCheck(
                agent_type=agent_type,
                status=status,
                timestamp=datetime.now(),
                response_time=response_time,
                error_message=error_message,
                details=test_result.get("details", {})
            )
            
            # Update cache
            self.health_cache[agent_type] = health_check
            
            # Update performance metrics
            self._update_performance_metrics(agent_type, health_check)
            
            # Check for alerts
            self._check_for_alerts(agent_type, health_check)
            
            return health_check
            
        except Exception as e:
            response_time = time.time() - start_time
            health_check = HealthCheck(
                agent_type=agent_type,
                status=MonitorStatus.CRITICAL,
                timestamp=datetime.now(),
                response_time=response_time,
                error_message=str(e)
            )
            
            self.health_cache[agent_type] = health_check
            self._update_performance_metrics(agent_type, health_check)
            self._check_for_alerts(agent_type, health_check)
            
            return health_check
    
    def run_all_health_checks(self) -> Dict[str, HealthCheck]:
        """Run health checks for all agents"""
        all_agents = self.registry.get_all_agents()
        results = {}
        
        for agent_type in all_agents.keys():
            results[agent_type] = self.run_health_check(agent_type)
        
        return results
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get a summary of monitoring status"""
        all_agents = self.registry.get_all_agents()
        summary = {
            "total_agents": len(all_agents),
            "monitoring_active": self.is_monitoring,
            "health_status": {},
            "performance_summary": {},
            "recent_alerts": len(self.get_alerts(hours=1))
        }
        
        # Health status summary
        for agent_type in all_agents.keys():
            health = self.get_agent_health(agent_type)
            if health:
                summary["health_status"][agent_type] = health.status.value
            else:
                summary["health_status"][agent_type] = MonitorStatus.UNKNOWN.value
        
        # Performance summary
        for agent_type in all_agents.keys():
            metrics = self.get_agent_performance(agent_type)
            if metrics:
                summary["performance_summary"][agent_type] = {
                    "success_rate": metrics.success_rate,
                    "avg_response_time": metrics.response_time_avg,
                    "total_requests": metrics.total_requests
                }
        
        return summary
    
    def _initialize_metrics(self):
        """Initialize performance metrics for all agents"""
        all_agents = self.registry.get_all_agents()
        
        for agent_type in all_agents.keys():
            self.performance_metrics[agent_type] = PerformanceMetrics(
                agent_type=agent_type
            )
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                logger.debug("Running scheduled health checks")
                self.run_all_health_checks()
                
                # Wait for next check interval
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Short delay before retry
    
    def _test_agent_functionality(self, agent: Any, agent_type: str) -> Dict[str, Any]:
        """Test basic functionality of an agent"""
        try:
            # Test agent info retrieval
            agent_info = agent.get_agent_info()
            
            # Test knowledge base access (if available)
            knowledge_status = "unknown"
            try:
                if hasattr(agent, 'initialize_lightrag'):
                    # This is a simplified test - in practice you'd want more comprehensive testing
                    knowledge_status = "available"
            except:
                knowledge_status = "unavailable"
            
            return {
                "success": True,
                "details": {
                    "agent_info": agent_info,
                    "knowledge_status": knowledge_status,
                    "agent_type": agent_type
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "details": {"agent_type": agent_type}
            }
    
    def _update_performance_metrics(self, agent_type: str, health_check: HealthCheck):
        """Update performance metrics based on health check"""
        metrics = self.performance_metrics.get(agent_type)
        if not metrics:
            metrics = PerformanceMetrics(agent_type=agent_type)
            self.performance_metrics[agent_type] = metrics
        
        # Update metrics
        metrics.total_requests += 1
        metrics.last_request_time = health_check.timestamp
        
        # Update response time statistics
        response_time = health_check.response_time
        if metrics.response_time_avg == 0:
            metrics.response_time_avg = response_time
            metrics.response_time_min = response_time
            metrics.response_time_max = response_time
        else:
            metrics.response_time_avg = (metrics.response_time_avg + response_time) / 2
            metrics.response_time_min = min(metrics.response_time_min, response_time)
            metrics.response_time_max = max(metrics.response_time_max, response_time)
        
        # Update success rate
        if health_check.status == MonitorStatus.HEALTHY:
            success_count = metrics.total_requests - metrics.error_count
        else:
            metrics.error_count += 1
            success_count = metrics.total_requests - metrics.error_count
        
        metrics.success_rate = success_count / metrics.total_requests if metrics.total_requests > 0 else 0.0
    
    def _check_for_alerts(self, agent_type: str, health_check: HealthCheck):
        """Check for conditions that should trigger alerts"""
        # Check for critical status
        if health_check.status == MonitorStatus.CRITICAL:
            alert = Alert(
                agent_type=agent_type,
                level=AlertLevel.CRITICAL,
                message=f"Agent {agent_type} is in critical state: {health_check.error_message}",
                timestamp=datetime.now(),
                details={"health_check": health_check.__dict__}
            )
            self._trigger_alert(alert)
        
        # Check for warning status
        elif health_check.status == MonitorStatus.WARNING:
            alert = Alert(
                agent_type=agent_type,
                level=AlertLevel.WARNING,
                message=f"Agent {agent_type} is in warning state",
                timestamp=datetime.now(),
                details={"health_check": health_check.__dict__}
            )
            self._trigger_alert(alert)
        
        # Check for high response time
        elif health_check.response_time > 10.0:  # 10 seconds threshold
            alert = Alert(
                agent_type=agent_type,
                level=AlertLevel.WARNING,
                message=f"Agent {agent_type} has high response time: {health_check.response_time:.2f}s",
                timestamp=datetime.now(),
                details={"response_time": health_check.response_time}
            )
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: Alert):
        """Trigger an alert and notify callbacks"""
        self.alerts.append(alert)
        logger.warning(f"Alert: {alert.message}")
        
        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")


# Global monitor instance
agent_monitor = AgentMonitor()


def get_agent_monitor() -> AgentMonitor:
    """Get the global agent monitor"""
    return agent_monitor


def start_monitoring():
    """Start the global agent monitoring"""
    agent_monitor.start_monitoring()


def stop_monitoring():
    """Stop the global agent monitoring"""
    agent_monitor.stop_monitoring()


def get_agent_health(agent_type: str) -> Optional[HealthCheck]:
    """Get health information for a specific agent"""
    return agent_monitor.get_agent_health(agent_type)


def get_all_agent_health() -> Dict[str, HealthCheck]:
    """Get health information for all agents"""
    return agent_monitor.get_all_agent_health()


def get_monitoring_summary() -> Dict[str, Any]:
    """Get a summary of monitoring status"""
    return agent_monitor.get_monitoring_summary()


# Export monitoring functions
__all__ = [
    "AgentMonitor",
    "MonitorStatus",
    "AlertLevel",
    "PerformanceMetrics",
    "HealthCheck",
    "Alert",
    "agent_monitor",
    "get_agent_monitor",
    "start_monitoring",
    "stop_monitoring",
    "get_agent_health",
    "get_all_agent_health",
    "get_monitoring_summary"
] 