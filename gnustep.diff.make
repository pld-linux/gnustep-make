--- GNUmakefile.in.old	Mon Nov 12 21:41:22 2001
+++ GNUmakefile.in	Mon Nov 12 21:41:30 2001
@@ -32,7 +32,7 @@
 # To install everything inside a temporary directory (say as part of
 # building a binary package - deb or rpm), use something like `make
 # install special_prefix=/var/tmp/gnustep-make'
-special_prefix = 
+special_prefix = @GNUSTEP_INSTALLATION_DIR@
 
 GNUSTEP_SYSTEM_ROOT = $(special_prefix)@prefix@
 GNUSTEP_LOCAL_ROOT  = $(special_prefix)@GNUSTEP_LOCAL_ROOT@
