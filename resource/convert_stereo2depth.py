import depthai as dai

pipeline = dai.Pipeline()
stereo = pipeline.create(dai.node.StereoDepth)

# Better handling for occlusions:
stereo.setLeftRightCheck(False)
# Closer-in minimum depth, disparity range is doubled:
stereo.setExtendedDisparity(False)
# Better accuracy for longer distance, fractional disparity 32-levels:
stereo.setSubpixel(False)

# Define and configure MonoCamera nodes beforehand
#left.out.link(stereo.left)
#right.out.link(stereo.right)