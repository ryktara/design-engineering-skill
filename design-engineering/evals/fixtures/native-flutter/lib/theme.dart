import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
ThemeData appTheme() => ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal, brightness: Brightness.light), textTheme: GoogleFonts.nunitoTextTheme(), cardTheme: const CardTheme(elevation: 0, shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(8)))));
