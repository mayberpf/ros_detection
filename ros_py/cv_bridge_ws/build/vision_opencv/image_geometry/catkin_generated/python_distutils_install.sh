#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/rpf/cv_bridge_ws/src/vision_opencv/image_geometry"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/rpf/cv_bridge_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/rpf/cv_bridge_ws/install/lib/python3/dist-packages:/home/rpf/cv_bridge_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/rpf/cv_bridge_ws/build" \
    "/usr/bin/python3" \
    "/home/rpf/cv_bridge_ws/src/vision_opencv/image_geometry/setup.py" \
    egg_info --egg-base /home/rpf/cv_bridge_ws/build/vision_opencv/image_geometry \
    build --build-base "/home/rpf/cv_bridge_ws/build/vision_opencv/image_geometry" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/rpf/cv_bridge_ws/install" --install-scripts="/home/rpf/cv_bridge_ws/install/bin"
