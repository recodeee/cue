/**
 * `cue audit` — profile audit commands.
 *
 * Subcommands:
 *   --security [profile]  Security audit (allowed-tools, MCPs, hooks, gates)
 *   (default)             Runs security audit
 */

export async function run(args: string[]): Promise<number> {
  if (args.includes("-h") || args.includes("--help")) {
    process.stdout.write(`cue audit — profile audit commands

Usage:
  cue audit --security [profile]   Security audit (tools, MCPs, hooks, gates)
  cue audit [profile]              Same as --security (default)

Examples:
  cue audit --security backend
  cue audit
`);
    return 0;
  }

  // Default to security audit
  const { runSecurityAudit } = await import("./security-audit");
  const filtered = args.filter(a => a !== "--security");
  return runSecurityAudit(filtered);
}
