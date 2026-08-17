#!/usr/bin/env node
//
// pre-commit.mjs — vérifie le formatage et la compilation avant le commit.
//
// Ce script est copié tel quel dans .husky/pre-commit.mjs au moment du
// `bootstrap init`, et invoqué par le shim .husky/pre-commit (husky exécute
// les hooks via `sh`, qui ne sait pas lancer du JavaScript directement).
// Il ne dépend plus de project-bootstrap : toute la configuration
// nécessaire (langages, extensions, checks) est lue dans
// bootstrap.config.json, écrit à la racine du dépôt au même moment.
//
// `bootstrap check` (CI) exécute ce même fichier pour garantir que le hook
// et la CI lancent exactement le même code.
//
// Contournement ponctuel : git commit --no-verify

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

function repoRoot() {
  const res = spawnSync("git", ["rev-parse", "--show-toplevel"], {
    encoding: "utf8",
  });
  if (res.status !== 0) {
    console.error("Impossible de déterminer la racine du dépôt Git.");
    process.exit(1);
  }
  return res.stdout.trim();
}

function gitFileList(args) {
  const res = spawnSync("git", ["diff", "--name-only", "--diff-filter=ACMR", ...args], {
    encoding: "utf8",
  });
  return res.stdout
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function loadConfig(root) {
  const configPath = path.join(root, "bootstrap.config.json");
  if (!fs.existsSync(configPath)) {
    // Pas de configuration : rien à vérifier, on laisse passer le commit.
    return [];
  }
  const raw = fs.readFileSync(configPath, "utf8");
  return JSON.parse(raw).languages ?? [];
}

function substitute(command, file) {
  return command.map((part) => (part === "{file}" ? file : part));
}

function runCheck(check, root, file) {
  const command = substitute(check.command, file ?? "");
  const res = spawnSync(command[0], command.slice(1), { cwd: root });

  if (res.error) {
    if (res.error.code === "ENOENT") {
      return {
        ok: false,
        message: `"${command[0]}" est introuvable : la règle "${check.id}" ne peut pas être appliquée. Installe l'outil ou commit avec --no-verify.`,
      };
    }
    return { ok: false, message: `Erreur en exécutant "${command[0]}" : ${res.error.message}` };
  }

  if (res.status !== 0) {
    const cible = file ?? "le projet";
    const hint = check.fixHint ? check.fixHint.replaceAll("{file}", file ?? "") : null;
    return {
      ok: false,
      message: `${cible} : la règle "${check.id}" a échoué${hint ? `\n    corriger : ${hint}` : ""}`,
    };
  }

  return { ok: true };
}

function main() {
  const root = repoRoot();
  const languages = loadConfig(root);

  const staged = gitFileList(["--cached"]).filter((f) => f.startsWith("project/"));

  if (staged.length === 0) {
    process.exit(0);
  }

  const unstagedChanges = new Set(gitFileList([]));
  const divergents = staged.filter((f) => unstagedChanges.has(f));
  if (divergents.length > 0) {
    console.log("Attention : ces fichiers ont des modifications non indexées.");
    console.log("L'analyse porte sur la version du disque, pas sur celle du commit.");
    for (const f of divergents) console.log(`    ${f}`);
    console.log("");
  }

  const failures = [];

  for (const language of languages) {
    const matched = staged.filter((f) => language.extensions.some((ext) => f.endsWith(ext)));
    if (matched.length === 0) continue;

    for (const check of language.checks ?? []) {
      if (check.scope === "file") {
        for (const file of matched) {
          const result = runCheck(check, root, file);
          if (!result.ok) failures.push(result.message);
        }
      } else if (check.scope === "project") {
        const result = runCheck(check, root, null);
        if (!result.ok) failures.push(result.message);
      }
    }
  }

  if (failures.length > 0) {
    console.error("Échec des vérifications pre-commit :\n");
    for (const message of failures) console.error(`  ${message}`);
    console.error("\nCommit annulé.");
    process.exit(1);
  }

  process.exit(0);
}

main();
