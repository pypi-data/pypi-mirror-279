from typing import Any, Self


class Singleton:
  """Keep single instance at all times.

  ## Make sure to put the `tcr.Singleton` inheretance before all others!
  ### ❌ `class A(B, tcr.Singleton)`
  ### ✅ `class A(tcr.Singleton, B)`

  ```py
  class SingleTuple(tcr.Singleton, tuple):
      ...

    tup = SingleTuple(('tup1',))
    tup2 = SingleTuple(('tup2',)) # Those arguments are effectively ignored

    console(tup)  # -> ('tup1',)
    console(tup2) # -> ('tup1',)
  ```
  """

  __singleton_instance__ = None

  def __new__(cls, *args, **kwargs) -> Self:
    if cls.__singleton_instance__ is None:
      cls.__singleton_instance__ = super().__new__(cls, *args, **kwargs)
    return cls.__singleton_instance__


class NoInit:
  def __init__(self, *args, **kwargs) -> None:
    msg = 'You cannot instiantiate this class'

    if hasattr(self, '__noinit_msg'):
      msg = str(getattr(self, '__noinit_msg'))

    raise RuntimeError(msg)


def partial_class(_f=None, /, *, add_as_kwargs_to_init: bool = True) -> type:
  """### Simillarly to functools.partial allows subclasses of decorated class to hold a meta-like state to be later used in e.g. root's init or anywhere else.

  ```py
  @tcr.partial_class
  class Button:
    def __init__(self, label: str):
      self.label = label

    def __repr__(self):
      return f'Button(label={self.label!r})'

  class YesButton(Button, label='Yes'): ...
  class NoButton(Button, label='No'): ...

  y = YesButton()
  c(repr(y)) # -> Button(label='Yes')
  n = NoButton()
  c(repr(n)) # -> Button(label='No')
  n2 = NoButton(label='Nuh uh') # Overridden
  c(repr(n2)) # -> Button(label='Nuh uh')
  ```

  Args:
    add_as_kwargs_to_init: bool = True. If True, the state  will be passed as keyword arguments into `__init__`.
  """

  def decorator(cls: type) -> type:
    def new_init_subclass(new_cls, **kwargs) -> None:
      new_cls._partial_state = kwargs

      if not add_as_kwargs_to_init:
        return

      original_init = new_cls.__init__

      def new_init(self, *args, **init_kwargs):
        merged_kwargs = {**self._partial_state, **init_kwargs}  # Merge both states such that caller can override it, like functools.partial
        original_init(self, *args, **merged_kwargs)

      new_cls.__init__ = new_init

    cls.__init_subclass__ = classmethod(new_init_subclass)
    return cls

  if _f is not None:
    return decorator(_f)
  return decorator


class DefaultsGetSetItem:
  def __getitem__(self, __key: Any) -> Any:
    try:
      return super().__getitem__(__key)
    except KeyError:
      if __key in self.defaults:
        val = self.defaults[__key]()
        self[__key] = val
        return val
      else:
        raise

class DefaultsGetItem:
  def __getitem__(self, __key: Any) -> Any:
    try:
      return super().__getitem__(__key)
    except KeyError:
      if __key in self.defaults:
        return self.defaults[__key]()
      else:
        raise

class DefaulstGetSetAttr:
  def __getattr__(self, __name: str) -> Any:
    try:
      return super().__getattr__(__name)
    except AttributeError:
      if __name in self.defaults:
        val = self.defaults[__name]()
        self.__setattr__(__name, val)
        return val
      else:
        raise

class DefaultsGetAttr:
  def __getattr__(self, __name: str) -> Any:
    try:
      return getattr(super(), __name)
    except AttributeError as e:
      if __name in self.defaults:
        return self.defaults[__name]()
      else:
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute nor default value for {__name!r}") from e
