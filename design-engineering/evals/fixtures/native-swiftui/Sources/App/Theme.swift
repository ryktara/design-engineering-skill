import SwiftUI
enum AppFont { static let body = Font.custom("Source Sans 3", size: 17); static let title = Font.system(.title2, design: .rounded).weight(.semibold) }
enum AppColor { static let canvas = Color(red: 0.98, green: 0.98, blue: 0.99); static let surface = Color.white }
struct CardStyle: ViewModifier { func body(content: Content) -> some View { content.padding(16).background(AppColor.surface).clipShape(RoundedRectangle(cornerRadius: 12)).shadow(radius: 2) } }
