
@HtmlImport('main_frame.html')
library main_frame;

import 'dart:html' as html;
import 'package:web_components/web_components.dart' show HtmlImport;
import 'package:polymer/polymer.dart';

import 'package:wasanbon_elements/wasanbon_toolbar.dart';
import 'package:wasanbon_elements/message_dialog.dart';

import 'package:wasanbon_xmlrpc/wasanbon_xmlrpc.dart' as wasanbon;

/// Global object for calling Remote Procedure Call for Wasanbon Server.
wasanbon.WasanbonRPC rpc;

@PolymerRegister('main-frame')
class MainFrame extends PolymerElement {

  MainFrame.created() : super.created();
  
  void attached() {
    ($$('#toolbar') as WasanbonToolbar).onBack.listen((var e) {
      onBack();
    });

    ConfirmDialog dlg = $$('#message-dlg');
    dlg.ptr.onOK.listen((var dlg_) {
      html.window.location.href='http://${Uri.base.host}:${Uri.base.port}';
    });


  }

  void onBack() {
    ConfirmDialog dlg = $$('#message-dlg');
    dlg.show('Confirm', 'Really exit from Apps?');
  }
}
