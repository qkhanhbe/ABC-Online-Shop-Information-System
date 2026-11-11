#!/bin/sh
# usage: run_mode.sh SOURCE.vpp "mode args"   (compile + install the plugin, then run one plugin mode headless)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
BSRC=C:/Users/bequo/AppData/Local/Temp/claude/ac202f680cce4163/4b7ac8b8-e5de-4160-88e2-5714c35c19bf/scratchpad/vpgen_bsrc
VP="${VPHOME:-/d/Visual Paradigm CE 18.1}"
JDK="/c/Program Files/Java/jdk-17/bin"
PLUG="$APPDATA/VisualParadigm/plugins/essay.gen"
rm -rf "$HERE/classes" "$BSRC" && mkdir -p "$HERE/classes" "$BSRC/vpmcp"
for f in "$HERE"/src/essay/gen/*.jsrc; do b=$(basename "$f" .jsrc); cp "$f" "$BSRC/$b.java"; done
for f in "$HERE"/third_party/vp-mcp/util/*.jsrc; do b=$(basename "$f" .jsrc); cp "$f" "$BSRC/vpmcp/$b.java"; done
"$JDK/javac.exe" --release 11 -nowarn -encoding UTF-8 -cp "$(cygpath -w "$VP/lib/openapi.jar");$(cygpath -w "$VP/lib/lib02.jar")" -d "$HERE/classes" "$BSRC"/*.java "$BSRC"/vpmcp/*.java
rm -rf "$PLUG" && mkdir -p "$PLUG" && cp -r "$HERE/classes" "$HERE/plugin.xml" "$PLUG/"
CP=".;../lib/vpplatform.jar;../lib/jniwrap.jar;../lib/winpack.jar;../ormlib/orm.jar;../ormlib/orm-core.jar;../lib/lib01.jar;../lib/lib02.jar;../lib/lib03.jar;../lib/lib04.jar;../lib/lib05.jar;../lib/lib06.jar;../lib/lib07.jar;../lib/lib08.jar;../lib/lib09.jar;../lib/lib10.jar"
cd "$VP/bin"
../jre/bin/java.exe -Xmx1200m -Djava.awt.headless=true -cp "$CP" com.vp.cmd.Plugin -project "$(cygpath -w "$1")" \
  -pluginid essay.gen -pluginargs "$2" > "$HERE/mode.log" 2>&1 || true
grep -v "wmic\|CreateProcess\|prefs\|BackingStore\|^getLicense\|startup" "$HERE/mode.log" | head -120
