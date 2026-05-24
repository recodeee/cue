/**
 * `cue quick [message]` — one-shot launch with zero skills/MCPs.
 *
 * Fastest possible cold start. No profile resolution, no materialization.
 * Just launches the real claude binary directly with an optional initial message.
 *
 * Usage:
 *   cue quick                     # launch bare claude
 *   cue quick "fix the typo"     # launch with initial prompt
 *   cue quick -p "summarize"     # pass -p flag through
 */

import { spawn } from "node:child_process";

import { findRealClaudeBin } from "../lib/claude-binary";

export async function run(args: string[]): Promise<number> {
  const realBin = findRealClaudeBin();
  if (!realBin) {
    process.stderr.write("cue quick: couldn't find the real 'claude' binary on PATH\n");
    return 127;
  }

  // Pass all args through to claude (e.g. -p "message", --model, etc.)
  const childArgs = args.length ? args : [];

  process.stderr.write("⚡ cue quick — launching bare claude (no profile)\n");

  return new Promise((res) => {
    const child = spawn(realBin, childArgs, {
      stdio: "inherit",
      env: { ...process.env, CUE_LAUNCHING: "1" },
    });
    child.on("exit", (code) => res(code ?? 0));
    child.on("error", () => res(127));
  });
}
