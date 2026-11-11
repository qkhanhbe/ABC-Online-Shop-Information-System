#!/bin/sh
# usage: relayout.sh SOURCE.vpp OUT.vpp PNG_DIR   (CE: hand layout from layout_spec.txt, then export)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
VP="/d/Visual Paradigm CE 18.1"
WORK="$(dirname "$2")/relayout_src.vpp"
cp "$1" "$WORK"
rm -rf "$3"
cd "$VP/bin"
CP=".;../lib/vpplatform.jar;../lib/jniwrap.jar;../lib/winpack.jar;../ormlib/orm.jar;../ormlib/orm-core.jar;../lib/lib01.jar;../lib/lib02.jar;../lib/lib03.jar;../lib/lib04.jar;../lib/lib05.jar;../lib/lib06.jar;../lib/lib07.jar;../lib/lib08.jar;../lib/lib09.jar;../lib/lib10.jar"
ARGS="relayout $(cygpath -w "$HERE/layout_spec.txt")|$(cygpath -w "$2")|$(cygpath -w "$3")"
../jre/bin/java.exe -Xmx1200m -Djava.awt.headless=true -cp "$CP" com.vp.cmd.Plugin -project "$(cygpath -w "$WORK")" \
  -pluginid essay.gen -pluginargs "$ARGS" > "$HERE/relayout.log" 2>&1 || true
grep -E "RELAYOUT|NOT FOUND|SAVED|EXPORT FAILED|Exception" "$HERE/relayout.log" | grep -v "wmic\|CreateProcess\|prefs\|BackingStore" | head -40
ls "$3" | wc -l
