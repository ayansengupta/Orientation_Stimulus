from warnings import warn
import copy as copy
import numpy as np

def gabor_patch(size, lambda_, theta, sigma, phase, trim=.005):
    """Create a Gabor Patch

    size : int
        Image size (n x n)

    lambda_ : int
        Spatial frequency (px per cycle)

    theta : int or float
        Grating orientation in degrees

    sigma : int or float
        gaussian standard deviation (in pixels)

    phase : float
        0 to 1 inclusive
    """
    # make linear ramp
    X0 = (np.linspace(1, size, size) / size) - .5

    # Set wavelength and phase
    freq = size / float(lambda_)
    phaseRad = phase * 2 * np.pi

    # Make 2D grating
    Xm, Ym = np.meshgrid(X0, X0)

    # Change orientation by adding Xm and Ym together in different proportions
    thetaRad = (theta / 360.) * 2 * np.pi
    Xt = Xm * np.cos(thetaRad)
    Yt = Ym * np.sin(thetaRad)
    grating = np.sin(((Xt + Yt) * freq * 2 * np.pi) + phaseRad)

    # 2D Gaussian distribution
    gauss = np.exp(-((Xm ** 2) + (Ym ** 2)) / (2 * (sigma / float(size)) ** 2))

    # Trim
    gauss[gauss < trim] = 0

   # return grating * gauss
    return grating

def gabor_color(arr, mask, patch):
    arr[mask] = patch[mask]
    return arr
    
def paint_plain_color(arr, mask, color):
    """Assign a uniform color to the entire array mask.

    Parameters
    ----------
    color : 3-tuple
      Color specification. Needs to match order and dtype of the array.
    """
    arr[mask] = color

def paint_speckled_color(arr, mask, color):
    """Assign a speckled color to the entire array mask.

    Parameters
    ----------
    color : 3-tuple
      Color specification. Needs to match order and dtype of the array.
    """
    arr[mask * np.random.random(mask.shape) > 0.5] = color

def get_quadrant_handled_width_list(width, qh_width_list):
    """
    The numpy.arctan2 function used in cart2pol returns angle in range -pi to pi. In order to handle the 
    patches ranging across different quadrants this method is introduced. It can handle the following four conditions. 
    """
    
    # when the patch of stimulus is within the first two quadrants
    if width[0]<=180 and width[1]<=180:
	qh_width_list.append((width[0], width[1]))
    
    # when the patch of stimulus is within the third or fourth quadrants
    if width[0]>=180 and width[1]>=180:
        qh_width_list.append((width[0]-360, width[1]-360))
    
    # when the patch of stimulus starts in quadrant 1 or quadrant 2 but extends into quadrant 3 or quadrant 4
    if width[0]<=180 and width[1]>=180:
        qh_width_list.append((width[0], 180))
        qh_width_list.append((-180, width[1]-360))
    
    # when the patch of stimulus starts in quadrant 3 or quadrant 4 but extends into quadrant 1 or quadrant 2
    if width[0]>=180 and (width[1]>=0 and width[1]<=180):
        qh_width_list.append((width[0]-360, 0))
        qh_width_list.append((0, width[1]))

    return qh_width_list

def get_circle_segment_mask(screen_shape, radius, width, center=None, phase=0):
    """Draw a colored circle segment

    Parameters
    ----------
    screen_shape : tuple
      Screen shape tuple (width, height)
    radius : 2-tuple
      Start and end angle of the segment distance from the center. Angles
      need to be sorted from low to high.
    width : 2-tuple / List of 2-tuples
      Start and end angle of the segment width. The zero-degrees
      reference has a positive y-coordinate directly above the center.
      Angles need to be sorted from low to high.
    center : 2-tuple, optional
      Circle center in array coordinates. If None, the geometrical array center
      is used.
    """
    # get center if not defined
    if center is None:
        center = tuple([d/2 for d in screen_shape])
    
    # handler for one tuple value / list of tuples
    
    if isinstance(width, list):
        width=width
    else:
        width=[width]
    
    # generate mask
    final_mask = np.zeros(screen_shape,bool)
    qh_width_list = []
     
    # determine quadrant handled width list 
    for w in width:
        qh_width_list = get_quadrant_handled_width_list(w, qh_width_list)
    
    for width in qh_width_list:
        arr = np.zeros(screen_shape)
        theta, rho = cart2pol(*np.mgrid[:arr.shape[0],
                                        :arr.shape[1]],
                              offx=center[0], offy=center[1], phase=phase)
        mask = rho >= radius[0]
        mask -= rho >= radius[1]
        mask *= theta >= width[0]
        mask *= theta <= width[1]
	final_mask+=mask
    
    return final_mask
    
def draw_quadrant_handled_circle_segment(arr, radius, width, brush, center=None):
    warn("DEPRECATED: replace by get_... and brush()")
    """
    Draws a quadrant handled circle segment.
    """
    if center is None:
        center = tuple([d/2 for d in arr.shape])

    mask = get_quadrant_handled_circle_segment_mask(arr.shape[0:2], radius, width, center)
    brush(arr, mask)

def draw_circle_segment(arr, radius, width, brush, phase=0, center=None):
    warn("DEPRECATED: replace by get_... and brush()")
    """
    Draws a colored circle segment
    """
    if center is None:
        center = tuple([d/2 for d in arr.shape])
    mask = get_circle_segment_mask(arr.shape[0:2], radius, width, center, phase)
    brush(arr, mask)

def cart2pol(x, y, offx=0, offy=0, phase=0):
    """
    Conversion from cartesian to polar coordinates
    """
    centered_x = x - offx
    centered_y = y - offy
    theta = np.arctan2(centered_y, centered_x)
    theta *= 180 / np.pi
    theta *= -1
    centered_x *= centered_x
    centered_y *= centered_y
    centered_x += centered_y
    rho = np.sqrt(centered_x)
    return (theta, rho)

def htmlcolor2rgb(colorstring):
    """
    Convert #RRGGBB to an (R, G, B) tuple
    """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b) 

def get_rgb_frame(size, bg_color=(128, 128, 128)):
    """
    Returns a frame with given size and color.
    """
    arr = np.ones(size + (3,), dtype=np.uint8)
    arr *= 128
    return arr

def vis_angle_to_pixel_conv(screen, screen_width_cm, distance_of_eye_from_screen, stim_size):
    
    tot_vis_angle = np.arctan2((screen_width_cm / 2), distance_of_eye_from_screen)*180 / 3.1415
    pix_per_vis_angle = np.shape(screen)[0] / tot_vis_angle    
    stim_size_pixel = pix_per_vis_angle * stim_size
    
    return stim_size_pixel
    
def test():
    #determine the screen size
    screen = get_rgb_frame((640, 1024))

    #please refer to "http://www.w3schools.com/html/html_colornames.asp" for
    #the colorcodes
    paint = htmlcolor2rgb('#ffffff')
    plain_brush = lambda arr, mask: paint_plain_color(arr, mask, paint)
    speckled_brush = lambda arr, mask: paint_speckled_color(arr, mask, paint)
    gabor_brush = lambda arr,mask: gabor_color(arr, mask, patch)
    """
    drawing the segment of a circle
    wedges and rings can be drawn easily by changing the radius and angle
    covered. 
    """
    
    radius_tuple = (vis_angle_to_pixel_conv(screen, 25.5, 100, 0.8), vis_angle_to_pixel_conv(screen, 25.5, 100, 7.6))
    quadrant_mask = get_circle_segment_mask(screen.shape[0:2], radius_tuple, [(100, 260)], center = (640, 512))
    
    for angle in [0, 45, 90, 135]:
        phase_index=0
        for phase in [0, 0.25, 0.5, 0.75]:
            
            screen = get_rgb_frame((640, 1024))
            
            gabor=gabor_patch(1024, vis_angle_to_pixel_conv(screen, 25.5, 100, 1.0)/1.4, angle, 1, phase, trim=.005)
            
            gabor = gabor[0:640,:]
            gabor_scaled=gabor-(np.min(gabor))
            gabor_scaled=gabor_scaled/np.max(gabor_scaled)*255
            #gabor_brush = lambda arr,mask: gabor_color(arr, mask, gabor)
            for i in range(3):
                    screen[:,:,i] = gabor_color(screen[:,:,i], quadrant_mask, gabor_scaled)
            
            import Image as img
            screen = img.fromarray(np.rollaxis(screen, 1, 0))
            phase_index+=1
            screen.save('orientation_images/LH_'+str(angle)+'_'+str(phase_index)+'.png')
            
	
if __name__ == '__main__':
    test()
