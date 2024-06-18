from .version import __version__
import numpy as np


def compute_image_distance_for_object_distance(object_distance, focal_length):
    """
    For an object in object_distance (g) infront of the optics, compute at what
    image_distance (b) behind the optics the image will be sharp.

                1
    b = -----------------
            1       1
          ----- - -----
            f       g

    Parameters
    ----------
    object_distance : float
        The distance from the object to the aperture's principal plane.
    focal_length : float
        The focal_length of the optics.

    Returns
    -------
    image_distance : float
    """
    return 1.0 / (1.0 / focal_length - 1.0 / object_distance)


def compute_object_distance_for_image_distance(image_distance, focal_length):
    """
    For an image_distance (b) behind the optics, compute the object_distance
    (g) that an object needs to be in, in order for it to create a sharp image.

                1
    g = -----------------
            1       1
          ----- - -----
            f       b

    Parameters
    ----------
    image_distance : float
        The distance from the sharp image to the aperture's principal plane.
    focal_length : float
        The focal_length of the optics.

    Returns
    -------
    object_distance : float
    """
    return 1.0 / (1.0 / focal_length - 1.0 / image_distance)


def cxcyb2xyz(cx, cy, image_distance, focal_length):
    """
    Transforms a point's coordinates from imaging space (cx, cy, b) to
    cartesian space (x,y,z) on an optics with a given focal-length.
    The z-axis is parallel to the optical axis.

    Parameters
    ----------
    cx : float
        Direction-cosine corresponding to point's x-coordinate.
    cy : float
        Direction-cosine corresponding to point's y-coordinate.
    image_distance : float
        Image-distance corresponding to where point's z-coordinate forms a
        shapr image.
    focal_length : float
        The optic's focal-length.

    Returns
    -------
    x : float
        Coordinate of a point in x.
    y : float
        Coordinate of a point in y.
    z : float
        Coordinate of a point in z, this is the object-distance.
    """
    object_distance = compute_object_distance_for_image_distance(
        image_distance=image_distance, focal_length=focal_length
    )
    x = np.tan(cx) * object_distance
    y = np.tan(cy) * object_distance
    return np.array([x, y, object_distance])


def xyz2cxcyb(x, y, z, focal_length):
    """
    Transforms a point's coordinates from cartesian space (x,y,z) to
    the imaging space (cx, cy, b) on an optics with a given focal-length.
    The z-axis is parallel to the optical axis.

    Parameters
    ----------
    x : float
        Coordinate of a point in x.
    y : float
        Coordinate of a point in y.
    z : float
        Coordinate of a point in z.
    focal_length : float
        The optic's focal-length.

    Returns
    -------
    [cx, cy, b] : np.array

    cx : float
        Direction-cosine corresponding to point's x-coordinate.
    cy : float
        Direction-cosine corresponding to point's y-coordinate.
    image_distance : float
        Image-distance corresponding to where point's z-coordinate forms a
        shapr image.
    """
    object_distance = z
    image_distance = compute_image_distance_for_object_distance(
        object_distance=object_distance, focal_length=focal_length
    )
    cx = np.arctan(x / object_distance)
    cy = np.arctan(y / object_distance)
    return np.array([cx, cy, image_distance])


def resolution_of_depth(
    object_distance,
    focal_length,
    aperture_diameter,
    diameter_of_pixel_projected_on_sensor_plane,
):
    """
    Estimate and return the upper (g_p) and lower (g_m) object-distance which
    mark the range in object-distance where a telescope sees a sharp picture of
    when its focus is set to object_distance.

    Parameters
    ----------
    object_distance : float
        The object-distance to where the telescope's focus is set to.
        This will set the telescope's screen-distance to match the required
        image-distance.
    focal_length : float
        The telescope's focal-length.
    aperture_diameter : float
        The diameter of the telescope's aperture.
    diameter_of_pixel_projected_on_sensor_plane : float
        The diameter of a photo-sensor in the telescope's plane of
        photo-sensors.

    reference
    ---------
    @article{bernlohr2013monte,
        author = {
            Bernlohr, K and Barnacka, A and Becherini, Yvonne and Bigas, O
            Blanch and Carmona, E and Colin, P and Decerprit, G and Di Pierro, F
            and Dubois, F and Farnier, Christian and others
        },
        journal = {Astroparticle Physics},
        pages = {171--188},
        publisher = {Elsevier},
        title = {
            {Monte} {Carlo} design studies for the {Cherenkov Telescope Array}
        },
        volume = {43},
        year = {2013},
    }
    """
    f = focal_length
    D = aperture_diameter
    p = diameter_of_pixel_projected_on_sensor_plane
    g = object_distance

    g_p = g * (1 + p * g / (2 * f * D))
    g_m = g * (1 - p * g / (2 * f * D))

    return g_p, g_m
