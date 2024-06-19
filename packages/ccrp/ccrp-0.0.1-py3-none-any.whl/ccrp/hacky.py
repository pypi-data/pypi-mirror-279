"""
Hacky way of allowing you to do

```py3
p = get_hacky_volcora()
p.line("this is some text")
```

Instead of

```py3
dev = usb.get_volcora_dev()
dev.write(usb.out_ep, commands.line("this is some text"))
```
"""

from inspect import getmembers, isfunction

from . import commands, usb


class HackyPrinter:
    def __init__(self, dev, out_ep, funcs):
        self.dev = dev
        self.out_ep = out_ep
        self.funcs = funcs

    def __call__(self, c):
        self.dev.write(self.out_ep, c)

    def __getattr__(self, attr):
        if attr in self.funcs.keys():

            def __patched(*args, **kwargs):
                return self.dev.write(self.out_ep, self.funcs[attr](*args, **kwargs))

            return __patched
        return self.__getattribute__(attr)


def get_hacky_volcora():
    dev = usb.get_volcora_dev()
    return HackyPrinter(dev, usb.out_ep, dict(getmembers(commands, isfunction)))
