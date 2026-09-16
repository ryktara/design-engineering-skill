// swift-tools-version: 5.9
// Streaks — a small SwiftUI habit tracker used as a research fixture.
//
// This manifest exposes the app sources as a library target so the code can be
// type-checked / indexed with SwiftPM tooling. To run it as an iPhone app, create
// an iOS App target in Xcode and add `Sources/Streaks` (the asset catalog is
// processed as a resource bundle; `StreaksApp.swift` carries the `@main` entry).

import PackageDescription

let package = Package(
    name: "Streaks",
    platforms: [
        .iOS(.v17)
    ],
    products: [
        .library(name: "Streaks", targets: ["Streaks"])
    ],
    targets: [
        .target(
            name: "Streaks",
            path: "Sources/Streaks",
            resources: [
                .process("Assets.xcassets")
            ]
        ),
        .testTarget(
            name: "StreaksTests",
            dependencies: ["Streaks"],
            path: "Tests/StreaksTests"
        )
    ]
)
