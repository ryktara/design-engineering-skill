// swift-tools-version:5.9
// Lumen — a documentary streaming app for Apple TV (tvOS).
// Package-style source tree; open with an Xcode tvOS app target that depends on LumenTV.
import PackageDescription

let package = Package(
    name: "Lumen",
    defaultLocalization: "en",
    platforms: [
        .tvOS(.v17)
    ],
    products: [
        .library(name: "LumenTV", targets: ["LumenTV"])
    ],
    targets: [
        .target(
            name: "LumenTV",
            path: "Sources/LumenTV",
            resources: [.process("Resources")]
        ),
        .testTarget(
            name: "LumenTVTests",
            dependencies: ["LumenTV"],
            path: "Tests/LumenTVTests"
        )
    ]
)
