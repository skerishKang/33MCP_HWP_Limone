# Windows HWP COM lifecycle — narrowed fix and remaining uncertainty

Date: 2026-10-15 KST
Scope: our repository `skerishKang/33MCP_HWP_Limone`, Draft PR #2. No external repositories or private customer documents involved.

## Observed source defects now addressed
1. Repeated `initialize_hwp` could call `pythoncom.CoInitialize()` several times without a matching per-call `CoUninitialize()`.
2. If COM initialization succeeded but dispatch/visibility failed, the COM apartment was left initialized.
3. `__del__` called `CoUninitialize()` on whichever Python thread finalized the controller; COM requires same-thread teardown.
4. An already initialized controller could reuse an HwpObject COM proxy from another thread without checks.

## Changes
- Store the COM-owning thread ID on successful initialization. Treat repeat calls from the same thread as no-op; fail closed for different threads.
- On any initialization failure after `CoInitialize`, clear live references and call `CoUninitialize` from that thread.
- Remove finalizer-driven COM cleanup. Add idempotent `close()`, only for the original thread. Never call `Quit()` on a possibly user-owned HWP session.
- On the MCP server's normal exit, call `close()` only when the run-loop thread is the COM owner. Do not release another thread's COM apartment.
- Keep public tool names/arguments and experimental opt-in behavior unchanged.

## Verification
- **35 mocked/unit tests PASS**, including new previously failing cases for failed dispatch, failed window setup, double-init, wrong-thread reuse/cleanup, and clean shutdown. No actual Hancom/HWP subprocess was launched.
- Python syntax compilation and `git diff --check` PASS.
- Real Windows COM operation, HWP reopen and crash prevention are **NOT VERIFIED**. The former `combase.dll` `0xC0000005` is an observed crash, but this code change is not proved to resolve it.

## Remaining risk and next acceptance
- FastMCP may execute tool calls on different threads, depending on its runtime. The current safety check deliberately rejects cross-thread COM reuse rather than allowing a crash. The production architecture may require a dedicated single-owner COM execution thread or one subprocess per HWP session.
- Do not repeatedly start/stop Hangul on a user's working machine to test this. Use a dedicated Windows/Hancom test environment with synthetic documents only.
- Acceptance: demonstrate connection without HWP auto-start, create synthetic document, save explicitly, reopen and inspect content; collect exact Windows/Hangul/Python/client version and any COM faults.
- Keep Draft PR #2 and experimental tools OFF by default until native evidence exists.

Tracking: [#5](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5), [#11](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11).
