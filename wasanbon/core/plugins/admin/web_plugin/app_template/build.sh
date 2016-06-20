PACKAGE_NAME=AppTemplate
VERSION=0.0.1
DESCRIPTION=""
ICON_FILE=icon.png
APP_FILE=application.yaml


function build() {
  echo "************************************************"
  echo "* "
  echo "* Building Application ("$PACKAGE_NAME-$VERSION")"
  echo "* "
  echo "************************************************"
  echo ""
  rm -rf $PACKAGE_NAME
  pub build
}

function clean() {
  echo "************************************************"
  echo "* "
  echo "* Cleaning up Application ("$PACKAGE_NAME-$VERSION")"
  echo "* "
  echo "************************************************"
  echo ""
  rm -rf $PACKAGE_NAME $PACKAGE_NAME.zip build $PACKAGE_NAME-*.zip *~
}

function pack() {
  echo "************************************************"
  echo "* "
  echo "* Packing Application ("$PACKAGE_NAME-$VERSION")"
  echo "* "
  echo "************************************************"
  echo ""
  if ! [ -d build ]; then 
    build
  fi
  cp -R build $PACKAGE_NAME
  cp $ICON_FILE $PACKAGE_NAME/
  cp $APP_FILE $PACKAGE_NAME/
  zip -rq $PACKAGE_NAME.zip $PACKAGE_NAME
}

function install() {
  echo "************************************************"
  echo "* "
  echo "* Installing Application ("$PACKAGE_NAME-$VERSION") to wasanbon's directory"
  echo "* "
  echo "************************************************"
  echo ""
  mv $PACKAGE_NAME.zip `wasanbon-admin.py web package_dir`
}

function upload() {
  echo "************************************************"
  echo "* "
  echo "* Uploading Application ("$PACKAGE_NAME-$VERSION") to wasanbon's directory"
  echo "* "
  echo "************************************************"
  echo ""

  if ! [ -e $PACKAGE_NAME.zip ];then
    pack
  fi
  cp $PACKAGE_NAME.zip $PACKAGE_NAME-$VERSION.zip
  wasanbon-admin.py web upload_appshare $PACKAGE_NAME-$VERSION.zip -d "$DESCRIPTION"
}


if [ $# -ne 1 ]; then
  build
  pack
  install
  exit 
fi

if [ "$1" = "build" ]; then
  build 
  pack
fi

if [ "$1" = "install" ]; then
  install
fi

if [ "$1" = "upload" ]; then
  upload
fi

if [ "$1" = "clean" ];then
  clean
fi


