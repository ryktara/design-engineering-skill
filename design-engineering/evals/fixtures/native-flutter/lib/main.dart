import 'package:flutter/material.dart';
void main() => runApp(MaterialApp(theme: appTheme(), home: Scaffold(bottomNavigationBar: NavigationBar(destinations: const []), body: const AnimatedPadding(duration: Duration(milliseconds: 100), padding: EdgeInsets.all(16), child: Text("hi")))));
