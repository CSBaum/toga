from rubicon.objc import *

from toga_cocoa.libs import *


class TogaIconView(NSTableCellView):

    @objc_method
    def initWithFrame_(self, frame: CGRect):
        self = ObjCInstance(send_super(__class__, self, 'initWithFrame:', frame))
        self.setAutoresizingMask_(NSViewWidthSizable)

        iv = NSImageView.alloc().initWithFrame(NSMakeRect(0, 0, 17, 20))
        tf = NSTextField.alloc().initWithFrame(NSMakeRect(0, 0, 200, 17))

        iv.setImageScaling_(NSImageScaleProportionallyUpOrDown)
        iv.setImageAlignment_(NSImageAlignment.Center.value)

        tf.setBordered(False)
        tf.setDrawsBackground(False)

        self.setImageView(iv)
        self.setTextField(tf)
        self.addSubview(iv)
        self.addSubview(tf)
        return self

    @objc_method
    def init(self):
        self = ObjCInstance(send_super(__class__, self, 'init'))
        self.setAutoresizingMask_(NSViewWidthSizable)

        iv = NSImageView.alloc().initWithFrame(NSMakeRect(0, 0, 17, 20))
        tf = NSTextField.alloc().initWithFrame(NSMakeRect(0, 0, 200, 17))

        iv.setImageScaling_(NSImageScaleProportionallyUpOrDown)
        iv.setImageAlignment_(NSImageAlignment.Center.value)

        tf.setBordered(False)
        tf.setDrawsBackground(False)

        self.setImageView(iv)
        self.setTextField(tf)
        self.addSubview(iv)
        self.addSubview(tf)
        return self

    @objc_method
    def setImage(self, image):
        if image is self.imageView.image:
            # don't do anything if image did not change
            return

        if image:
            self.imageView.image = image
            self.imageView.frame = NSMakeRect(5, 0, 17, 17)
            self.textField.frame = NSMakeRect(25, 0, 200, 17)
        else:
            self.imageView.image = None
            self.imageView.frame = NSMakeRect(0, 0, 0, 0)
            self.textField.frame = NSMakeRect(0, 0, 200, 17)

    @objc_method
    def setText(self, text):
        if text != self.textField.stringValue:
            self.textField.stringValue = text


class TogaIconCell(NSTextFieldCell):

    @objc_method
    def drawWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        try:
            label = self.objectValue.attrs['label']
            icon = self.objectValue.attrs['icon']
        except AttributeError:
            # Value is a simple string.
            label = self.objectValue
            icon = None

        if icon and icon.native:
            offset = 28.5

            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y
            if view.isFlipped:
                xform = NSAffineTransform.transform()
                xform.translateXBy(8, yBy=cellFrame.size.height)
                xform.scaleXBy(1.0, yBy=-1.0)
                xform.concat()
                yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = NSImageInterpolationHigh

            icon.native.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset), NSSize(16.0, 16.0)),
                fromRect=NSRect(NSPoint(0, 0), NSSize(icon.native.size.width, icon.native.size.height)),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            # No icon; just the text label
            offset = 5

        if label:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(13)

            at(label).drawAtPoint(
                NSPoint(cellFrame.origin.x + offset, cellFrame.origin.y),
                withAttributes=textAttributes
            )


# A TogaDetailedCell contains:
# * an icon
# * a main label
# * a secondary label
class TogaDetailedCell(NSTextFieldCell):
    @objc_method
    def drawInteriorWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        icon = self.objectValue.attrs['icon']
        title = self.objectValue.attrs['title']
        subtitle = self.objectValue.attrs['subtitle']

        if icon and icon.native:
            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y
            if view.isFlipped:
                xform = NSAffineTransform.transform()
                xform.translateXBy(4, yBy=cellFrame.size.height)
                xform.scaleXBy(1.0, yBy=-1.0)
                xform.concat()
                yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = NSImageInterpolationHigh

            icon.native.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset + 4), NSSize(40.0, 40.0)),
                fromRect=NSRect(NSPoint(0, 0), NSSize(icon.native.size.width, icon.native.size.height)),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            path = NSBezierPath.bezierPathWithRect(
                NSRect(NSPoint(cellFrame.origin.x, cellFrame.origin.y + 4), NSSize(40.0, 40.0))
            )
            NSColor.grayColor.set()
            path.fill()

        if title:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(15)

            at(title).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 4),
                withAttributes=textAttributes
            )

        if subtitle:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(13)

            at(subtitle).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 24),
                withAttributes=textAttributes
            )
