"""Remove the fixed wait on the plugin / script import warning dialog.

``ok-script`` ships ``ok.ui.qt.widget.ImportWarningDialog`` with a hard coded
15 second countdown: even after ticking the risk acknowledgement, the Confirm
button stays disabled until the timer runs out. The delay adds nothing to the
safety of the dialog, it only slows down plugin installation.

This module rewires ``ImportWarningDialog.__init__`` at runtime, so the import
still shows the same warning text and still requires the risk checkbox, but the
Confirm button unlocks the moment the box is ticked.

The installed ``site-packages`` copy is never edited, therefore an ok-script
version bump cannot conflict with this patch. If a future release renames the
timer or the button, the patch degrades to a no-op instead of raising.
"""

from __future__ import annotations

_PATCH_FLAG = "_countdown_removed"


def apply() -> bool:
    """Install the patch once. Returns True when it is in place."""
    try:
        from ok.ui.qt.widget.ImportWarningDialog import ImportWarningDialog
    except Exception:
        return False

    if getattr(ImportWarningDialog, _PATCH_FLAG, False):
        return True

    original_init = ImportWarningDialog.__init__

    def init_without_countdown(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        timer = getattr(self, "timer", None)
        if timer is not None:
            try:
                timer.stop()
            except Exception:
                pass

        # ``check_state_changed`` unlocks the button when countdown <= 0.
        self.countdown = 0

        button = getattr(self, "yesButton", None)
        if button is not None:
            try:
                button.setText(self.tr("Confirm"))
            except Exception:
                pass

        try:
            self.check_state_changed()
        except Exception:
            pass

    ImportWarningDialog.__init__ = init_without_countdown
    setattr(ImportWarningDialog, _PATCH_FLAG, True)
    return True


PATCHED = apply()
