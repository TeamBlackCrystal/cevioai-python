"""
CeVIO AI RemoteService2 API Python wrapper.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Any
import os
import clr

_DOTNET_TYPES: dict[str, Any] | None = None


class HostStartResult(IntEnum):
	"""StartHost() result codes."""

	Succeeded = 0
	NotRegistered = -1
	FileNotFound = -2
	StartingFailed = -3
	HostError = -4


class HostCloseMode(IntEnum):
	"""CloseHost() mode."""

	Default = 0


def _default_install_dir() -> str:
	program_root = os.environ.get("ProgramW6432") or os.environ.get("ProgramFiles", "")
	return os.path.join(program_root, "CeVIO", "CeVIO AI")


def _resolve_dll_path(install_dir: str | None, dll_path: str | None) -> str:
	if dll_path:
		return dll_path
	base_dir = install_dir or _default_install_dir()
	return os.path.join(base_dir, "CeVIO.Talk.RemoteService2.dll")


def _load_dotnet_types(
	install_dir: str | None = None,
	dll_path: str | None = None,
	assembly_name: str = "CeVIO.Talk.RemoteService2",
) -> dict[str, Any]:
	global _DOTNET_TYPES
	if _DOTNET_TYPES is not None:
		return _DOTNET_TYPES

	resolved_dll_path = _resolve_dll_path(install_dir, dll_path)
	if not os.path.isfile(resolved_dll_path):
		raise FileNotFoundError(f"CeVIO AI DLL not found: {resolved_dll_path}")

	clr.AddReference(resolved_dll_path)

	try:
		from CeVIO.Talk.RemoteService2 import (  # type: ignore
			Talker2 as DotNetTalker2,
			TalkerComponentCollection2 as DotNetTalkerComponentCollection2,
			TalkerComponent2 as DotNetTalkerComponent2,
			SpeakingState2 as DotNetSpeakingState2,
			PhonemeData2 as DotNetPhonemeData2,
			ServiceControl2 as DotNetServiceControl2,
			HostStartResult as DotNetHostStartResult,
			HostCloseMode as DotNetHostCloseMode,
		)
	except Exception as exc:  # pragma: no cover - import-time failure
		raise ImportError(
			"Failed to import CeVIO.Talk.RemoteService2 types. "
			"Confirm the DLL version and assembly name."
		) from exc

	_DOTNET_TYPES = {
		"Talker2": DotNetTalker2,
		"TalkerComponentCollection2": DotNetTalkerComponentCollection2,
		"TalkerComponent2": DotNetTalkerComponent2,
		"SpeakingState2": DotNetSpeakingState2,
		"PhonemeData2": DotNetPhonemeData2,
		"ServiceControl2": DotNetServiceControl2,
		"HostStartResult": DotNetHostStartResult,
		"HostCloseMode": DotNetHostCloseMode,
	}
	return _DOTNET_TYPES


def _as_list(value: Any) -> list[Any]:
	return list(value) if value is not None else []


def _as_enum_value(value: Any, enum_type: type[IntEnum]) -> IntEnum:
	if isinstance(value, enum_type):
		return value
	if hasattr(value, "value"):
		return enum_type(int(value.value))
	if isinstance(value, str):
		try:
			return enum_type[value]
		except KeyError:
			return enum_type(enum_type.Succeeded)
	return enum_type(int(value))


class TalkerComponent2:
	"""Emotion parameter item wrapper."""

	def __init__(self, dotnet_component: Any):
		self._component = dotnet_component

	@property
	def id(self) -> str:
		return self._component.Id

	@property
	def name(self) -> str:
		return self._component.Name

	@property
	def value(self) -> int:
		return int(self._component.Value)

	@value.setter
	def value(self, value: int) -> None:
		self._component.Value = int(value)


class TalkerComponentCollection2:
	"""Emotion parameter map wrapper."""

	def __init__(self, dotnet_collection: Any):
		self._collection = dotnet_collection

	@property
	def count(self) -> int:
		return int(self._collection.Count)

	def __len__(self) -> int:
		return self.count

	def __getitem__(self, key: int | str) -> TalkerComponent2:
		return TalkerComponent2(self._collection[key])


class SpeakingState2:
	"""Speaking state wrapper."""

	def __init__(self, dotnet_state: Any):
		self._state = dotnet_state

	@property
	def is_completed(self) -> bool:
		return bool(self._state.IsCompleted)

	@property
	def is_succeeded(self) -> bool:
		return bool(self._state.IsSucceeded)

	def wait(self, timeout: float | None = None) -> None:
		if timeout is None:
			self._state.Wait()
		else:
			self._state.Wait(float(timeout))


class PhonemeData2:
	"""Phoneme data wrapper."""

	def __init__(self, dotnet_phoneme: Any):
		self._phoneme = dotnet_phoneme

	@property
	def phoneme(self) -> str:
		return self._phoneme.Phoneme

	@property
	def start_time(self) -> float:
		return float(self._phoneme.StartTime)

	@property
	def end_time(self) -> float:
		return float(self._phoneme.EndTime)


class Talker2:
	"""CeVIO AI talker wrapper."""

	def __init__(
		self,
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> None:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		self._talker = dotnet_types["Talker2"]()
		self._dotnet_types = dotnet_types

	@property
	def volume(self) -> int:
		return int(self._talker.Volume)

	@volume.setter
	def volume(self, value: int) -> None:
		self._talker.Volume = int(value)

	@property
	def speed(self) -> int:
		return int(self._talker.Speed)

	@speed.setter
	def speed(self, value: int) -> None:
		self._talker.Speed = int(value)

	@property
	def tone(self) -> int:
		return int(self._talker.Tone)

	@tone.setter
	def tone(self, value: int) -> None:
		self._talker.Tone = int(value)

	@property
	def alpha(self) -> int:
		return int(self._talker.Alpha)

	@alpha.setter
	def alpha(self, value: int) -> None:
		self._talker.Alpha = int(value)

	@property
	def tone_scale(self) -> int:
		return int(self._talker.ToneScale)

	@tone_scale.setter
	def tone_scale(self, value: int) -> None:
		self._talker.ToneScale = int(value)

	@property
	def components(self) -> TalkerComponentCollection2:
		return TalkerComponentCollection2(self._talker.Components)

	@property
	def cast(self) -> str:
		return self._talker.Cast

	@cast.setter
	def cast(self, value: str) -> None:
		self._talker.Cast = value

	@classmethod
	def available_casts(
		cls,
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> list[str]:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		raw_casts = dotnet_types["Talker2"].AvailableCasts
		return [str(item) for item in _as_list(raw_casts)]

	def speak(self, text: str) -> SpeakingState2:
		return SpeakingState2(self._talker.Speak(text))

	def stop(self) -> bool:
		return bool(self._talker.Stop())

	def get_text_duration(self, text: str) -> float:
		return float(self._talker.GetTextDuration(text))

	def get_phonemes(self, text: str) -> list[PhonemeData2]:
		return [PhonemeData2(item) for item in _as_list(self._talker.GetPhonemes(text))]

	def output_wave_to_file(self, text: str, path: str) -> bool:
		return bool(self._talker.OutputWaveToFile(text, path))


class ServiceControl2:
	"""CeVIO AI service control wrapper."""

	@staticmethod
	def host_version(
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> str:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		return str(dotnet_types["ServiceControl2"].HostVersion)

	@staticmethod
	def is_host_started(
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> bool:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		return bool(dotnet_types["ServiceControl2"].IsHostStarted)

	@staticmethod
	def start_host(
		no_wait: bool,
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> HostStartResult:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		result = dotnet_types["ServiceControl2"].StartHost(bool(no_wait))
		return _as_enum_value(result, HostStartResult)

	@staticmethod
	def close_host(
		mode: HostCloseMode = HostCloseMode.Default,
		install_dir: str | None = None,
		dll_path: str | None = None,
		assembly_name: str = "CeVIO.Talk.RemoteService2",
	) -> None:
		dotnet_types = _load_dotnet_types(install_dir, dll_path, assembly_name)
		dotnet_mode_type = dotnet_types.get("HostCloseMode")
		if dotnet_mode_type is not None:
			try:
				mode_value = dotnet_mode_type(int(mode))
			except Exception:
				mode_value = int(mode)
		else:
			mode_value = int(mode)
		dotnet_types["ServiceControl2"].CloseHost(mode_value)


__all__ = [
	"HostStartResult",
	"HostCloseMode",
	"Talker2",
	"TalkerComponentCollection2",
	"TalkerComponent2",
	"SpeakingState2",
	"PhonemeData2",
	"ServiceControl2",
]
