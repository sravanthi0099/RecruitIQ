"""Base agent class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger
import time


class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            version: Agent version
        """
        self.name = name
        self.version = version
        self.created_at = datetime.utcnow()

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent action.
        
        Args:
            input_data: Input data
            
        Returns:
            Agent result
        """
        pass

    def _log_execution(
        self,
        status: str,
        input_data: Dict[str, Any],
        output_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ):
        """
        Log agent execution.
        
        Args:
            status: Execution status
            input_data: Input data
            output_data: Output data
            error: Error message
            duration_ms: Execution duration in ms
        """
        logger.info(
            f"{self.name} execution",
            extra={
                "agent": self.name,
                "status": status,
                "duration_ms": duration_ms,
                "error": error,
            },
        )

    async def _execute_with_logging(
        self,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute agent with logging.
        
        Args:
            input_data: Input data
            
        Returns:
            Agent result with metadata
        """
        start_time = time.time()
        result = {
            "agent": self.name,
            "version": self.version,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
        }

        try:
            output = await self.execute(input_data)
            result["result"] = output
            result["status"] = "completed"
        except Exception as e:
            logger.error(f"Error in {self.name}: {str(e)}", exc_info=True)
            result["status"] = "failed"
            result["error"] = str(e)

        duration_ms = (time.time() - start_time) * 1000
        result["duration_ms"] = round(duration_ms, 2)
        self._log_execution(result["status"], input_data, duration_ms=duration_ms)

        return result

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, version={self.version})>"