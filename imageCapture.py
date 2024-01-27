import mss.tools
import mss


def capture():
    sct = mss.mss()
    monitor = sct.monitors[3]
    print("capture")
    output = "output\\output.png".format(**monitor)
    

    sct_img = sct.grab(monitor)

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)


if __name__ == "__main__":
    capture()