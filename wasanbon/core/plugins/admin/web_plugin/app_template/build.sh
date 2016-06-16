PACKAGE_NAME=AppTemplate
VERSION=0.0.1
ICON_FILE=icon.png

rm -rf $PACKAGE_NAME
pub build
mv build $PACKAGE_NAME
cp $ICON_FILE $PACKAGE_NAME/
zip -rq $PACKAGE_NAME.zip $PACKAGE_NAME
mv $PACKAGE_NAME.zip `wasanbon-admin.py web package_dir`
