# Gazebo Python 3.11 bindings
This package contains the Python bindings extracted from the Gazebo project, specifically packaged for use with Python 3.11 on x86_64 Linux distributions.

# Versions
- Gazebo: Harmonic
    - gz-math7
    - gz-transport13
    - gz-sim8
    - gz-common5
    - sdformat14
- Python: 3.11.4
- pybind11: 2.12.0

# Commit Hashes
Please refer to the commit hashes for the Gazebo project for the exact versions used in this package.

| Module         | Commit Hash                           |
|----------------|---------------------------------------|
| gz-cmake       | ddd38ff196640024d6e054ff59cf5fea1ef01d73 |
| gz-common      | 27f7017c5c1b1fd2ba9c603e92b694f98417175d |
| gz-fuel-tools  | e808b0ab580bdf9b413e28ba96a5bede978e5c98 |
| gz-gui         | 1a04fbb127e2e7de7df352a2a915a448f5710231 |
| gz-launch      | 2cb58a1e5add0017dd229f9090aea7614ae18930 |
| gz-math        | 02e37a63e9e24959424e1b2463a6dbe9195a79bb |
| gz-msgs        | 876b89d5cab32d9ddfd5f95ce8cf365ce77f27ef |
| gz-physics     | b5d1508bb7011240d64755506b599c5cd3f18ffa |
| gz-plugin      | e296968d2e4013d9d8c95d31c1f7b4dd5d2e87d8 |
| gz-rendering   | f3d30738726d11d240907e30699ce4c66e8a0f50 |
| gz-sensors     | 4d2ae188117486fbdc4b3a3df3fe25d539a8800d |
| gz-sim         | f024ea83dd26d3711976544a835b74d030cccdb0 |
| gz-tools       | 2b228e5b956f1e966053dd860374670573580b41 |
| gz-transport   | a5af52592810c2aa4f2fec417cc736a18f616e93 |
| gz-utils       | fd618d23156f754726fcd641934d908c766c8f75 |
| sdformat       | fc84f94d147bf31fd594e17bade68946246236b3 |

# Warning
- Please note that this package is specifically designed for Python 3.11 on x86_64 Linux distributions. It is not intended to be a universal distribution and may not function as expected on other Python versions or operating systems.
- Modifications to the CMake scripts were made to support the Python 3.11 build.
- Note the diffs below have been modified to redact personal information.

# Diff - gz-math
```
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 8e1e0be5..7914336a 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -115,7 +115,7 @@ else()
       set(Python3_VERSION ${PYTHONLIBS_VERSION_STRING})
     endif()
   else()
-    find_package(Python3 QUIET COMPONENTS Interpreter Development)
+    find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)
   endif()
 
   if (NOT Python3_FOUND)
@@ -124,8 +124,9 @@ else()
   else()
     message (STATUS "Searching for Python3 - found version ${Python3_VERSION}.")
 
-    set(PYBIND11_PYTHON_VERSION 3)
-    find_package(pybind11 2.2 QUIET)
+    set(PYBIND11_PYTHON_VERSION 3.11)
+    set(pybind11_DIR "/home/_REDACTED_/.local/lib/python3.11/site-packages/pybind11/share/cmake/pybind11")
+    find_package(pybind11 2.12.0 REQUIRED EXACT CONFIG)
 
     if (${pybind11_FOUND})
       message (STATUS "Searching for pybind11 - found version ${pybind11_VERSION}.")
```

# Diff - gz-transport
```
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 527e6cda..938ec08b 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -56,15 +56,15 @@ message(STATUS "\n\n-- ====== Finding Dependencies ======")
 # Python interfaces
 if (SKIP_PYBIND11)
   message(STATUS "SKIP_PYBIND11 set - disabling python bindings")
-  find_package(Python3 COMPONENTS Interpreter)
+  find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter)
 else()
-  find_package(Python3 COMPONENTS Interpreter Development)
+  find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)
   if (NOT Python3_Development_FOUND)
     GZ_BUILD_WARNING("Python development libraries are missing: Python interfaces are disabled.")
   else()
-    set(PYBIND11_PYTHON_VERSION 3)
-    find_package(pybind11 2.4 CONFIG QUIET)
-
+    set(PYBIND11_PYTHON_VERSION 3.11)
+    set(pybind11_DIR "/home/_REDACTED_/.local/lib/python3.11/site-packages/pybind11/share/cmake/pybind11")
+    find_package(pybind11 2.12.0 REQUIRED EXACT CONFIG)
     if (pybind11_FOUND)
       message (STATUS "Searching for pybind11 - found version ${pybind11_VERSION}.")
     else()
```

# Diff - gz-sim
```
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 30236494c..ff5a3e9f3 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -203,18 +203,21 @@ set(Protobuf_IMPORT_DIRS ${gz-msgs10_INCLUDE_DIRS})
 
 #--------------------------------------
 # Find python
+#--------------------------------------
 if (SKIP_PYBIND11)
   message(STATUS "SKIP_PYBIND11 set - disabling python bindings")
 else()
-  find_package(Python3 QUIET COMPONENTS Interpreter Development)
+  # Manually set the path to the Python 3.11 interpreter and development libraries
+  find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)
   if (NOT Python3_FOUND)
     GZ_BUILD_WARNING("Python is missing: Python interfaces are disabled.")
     message (STATUS "Searching for Python - not found.")
   else()
-    message (STATUS "Searching for Python - found version ${PYTHONLIBS_VERSION_STRING}.")
+    message (STATUS "Searching for Python - found version ${Python3_VERSION}.")
 
-    set(PYBIND11_PYTHON_VERSION 3)
-    find_package(pybind11 2.9 CONFIG QUIET)
+    set(PYBIND11_PYTHON_VERSION 3.11)
+    set(pybind11_DIR "/home/_REDACTED_/.local/lib/python3.11/site-packages/pybind11/share/cmake/pybind11")
+    find_package(pybind11 2.12.0 REQUIRED EXACT CONFIG)
 
     if (pybind11_FOUND)
       message (STATUS "Searching for pybind11 - found version ${pybind11_VERSION}.")
```