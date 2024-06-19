from typing import Dict
from typing import Optional


class KubernetesOptions:
    def __init__(
        self,
        replicas: int = 1,
        requests: Optional[Dict[str, str]] = None,
        limits: Optional[Dict[str, str]] = None,
        affinity: Optional[str] = None,
        toleration: Optional[str] = None,
    ):
        self._replicas = replicas
        self._requests = requests
        self._limits = limits
        self._affinity = affinity
        self._toleration = toleration

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"replicas: {self.replicas}\n"
            f"requests: {self.requests}\n"
            f"limits: {self.limits}\n"
            f"affinity: {self.affinity}\n"
            f"toleration: {self.toleration}"
        )

    @property
    def replicas(self) -> int:
        return self._replicas

    @replicas.setter
    def replicas(self, x: int) -> None:
        self._replicas = x

    @property
    def requests(self) -> Optional[Dict[str, str]]:
        return self._requests

    @requests.setter
    def requests(self, x: Optional[Dict[str, str]]) -> None:
        self._requests = x

    @property
    def limits(self) -> Optional[Dict[str, str]]:
        return self._limits

    @limits.setter
    def limits(self, x: Optional[Dict[str, str]]) -> None:
        self._limits = x

    @property
    def affinity(self) -> Optional[str]:
        return self._affinity

    @affinity.setter
    def affinity(self, x: Optional[str]) -> None:
        self._affinity = x

    @property
    def toleration(self) -> Optional[str]:
        return self._toleration

    @toleration.setter
    def toleration(self, x: Optional[str]) -> None:
        self._toleration = x


class MonitoringOptions:
    def __init__(self, enable: bool = True, save_scoring_inputs: bool = False):
        self._enable = enable
        self._save_scoring_inputs = save_scoring_inputs

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"enable: {self.enable}\n"
            f"save_scoring_inputs: {self.save_scoring_inputs}"
        )

    @property
    def enable(self) -> bool:
        return self._enable

    @enable.setter
    def enable(self, value: bool) -> None:
        self._enable = value

    @property
    def save_scoring_inputs(self) -> bool:
        return self._save_scoring_inputs

    @save_scoring_inputs.setter
    def save_scoring_inputs(self, value: bool) -> None:
        self._save_scoring_inputs = value


class SecurityOptions:
    def __init__(
        self, passphrase: Optional[str] = None, hashed_passphrase: Optional[bool] = None
    ):
        self._passphrase = passphrase
        self._hashed_passphrase = hashed_passphrase

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'>"

    def __str__(self) -> str:
        return (
            f"passphrase: {self.passphrase}\n"
            f"hashed_passphrase: {self.hashed_passphrase}"
        )

    @property
    def passphrase(self) -> Optional[str]:
        return self._passphrase

    @passphrase.setter
    def passphrase(self, x: Optional[str]) -> None:
        self._passphrase = x

    @property
    def hashed_passphrase(self) -> Optional[bool]:
        return self._hashed_passphrase

    @hashed_passphrase.setter
    def hashed_passphrase(self, x: Optional[bool]) -> None:
        self._hashed_passphrase = x
