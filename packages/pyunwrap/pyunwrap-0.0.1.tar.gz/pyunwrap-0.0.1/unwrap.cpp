#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <limits>
#include <algorithm>

namespace py = pybind11;

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

//PIXELM information
struct PIXELM {
  int increment; //No. of 2*pi to add to the pixel to unwrap it
  int number_of_pixels_in_group; //No. of pixel in the pixel group
  float value; //value of the pixel
  float reliability; // the lower the better
  struct PIXELM * head; //pointer to the first pixel in the group in the linked list
  struct PIXELM * last; //pointer to the last pixel in the group
  struct PIXELM * next; //pointer to the next pixel in the group
};

typedef struct PIXELM PIXELM;

//the EDGE is the line that connects two pixels.
//if we have S pixels, then we have S horizontal edges and S vertical edges
struct EDGE {
  float reliab; //reliabilty of the edge and it depends on the two pixels
  PIXELM * pointer_1; //pointer to the first pixel
  PIXELM * pointer_2; //pointer to the second pixel
  int increment; //No. of 2*pi to add to one of the pixels to
  //unwrap it with respect to the second
};

typedef struct EDGE EDGE;

//---------------start quicker_sort algorithm --------------------------------
#define swap(x, y) {EDGE t;t = x;x = y;y = t;}
#define order(x, y) if (x.reliab > y.reliab) swap(x, y)
#define o2(x, y) order(x, y)
#define o3(x, y, z) o2(x, y); o2(x, z); o2(y, z)

bool find_pivot(EDGE * left, EDGE * right, float * pivot_ptr) {
  EDGE a, b, c, * p;

  a = * left;
  b = * (left + (right - left) / 2);
  c = * right;
  o3(a, b, c);

  if (a.reliab < b.reliab) {
    * pivot_ptr = b.reliab;
    return true;
  }

  if (b.reliab < c.reliab) {
    * pivot_ptr = c.reliab;
    return true;
  }

  for (p = left + 1; p <= right; ++p) {
    if (p -> reliab != left -> reliab) {
      * pivot_ptr = (p -> reliab < left -> reliab) ? left -> reliab : p -> reliab;
      return true;
    }
    return false;
  }

  return false;
}

EDGE * partition(EDGE * left, EDGE * right, float pivot) {
  while (left <= right) {
    while (left -> reliab < pivot)
      ++left;
    while (right -> reliab >= pivot)
      --right;
    if (left < right) {
      swap( * left, * right);
      ++left;
      --right;
    }
  }
  return left;
}

void quicker_sort(EDGE * left, EDGE * right) {
  EDGE * p;
  float pivot;

  if (find_pivot(left, right, & pivot)) {
    p = partition(left, right, pivot);
    quicker_sort(left, p - 1);
    quicker_sort(p, right);
  }
}
//--------------end quicker_sort algorithm -----------------------------------

//initialize pixels. See the explination of the pixel class above.
//initially every pixel is assumed to belong to a group consisting of only itself
void initialisePIXELs(float * wrapped_image, float * quality_image, PIXELM * pixel, int width, int height) {
  for (int k = 0; k < height * width; k++) {
    pixel[k].increment = 0;
    pixel[k].number_of_pixels_in_group = 1;
    pixel[k].value = wrapped_image[k];
    pixel[k].reliability = 1.0/quality_image[k];
    pixel[k].head = & pixel[k];
    pixel[k].last = & pixel[k];
    pixel[k].next = NULL;
  }
}

int sign_wrap(float difference) {
  int wrap_value;
  if (difference > 0.5) wrap_value = -1;
  else if (difference < -0.5) wrap_value = 1;
  else wrap_value = 0;
  return wrap_value;
}

//gamma function in the paper
float wrap(float pixel_value) {
  return pixel_value+sign_wrap(pixel_value);
}

// pixelL_value is the left pixel,	pixelR_value is the right pixel
int find_wrap(float pixelL_value, float pixelR_value) {
  float difference = pixelL_value - pixelR_value;
  return sign_wrap(difference);
}

void calculate_reliability(float * wrapped, float * quality, PIXELM * pixel, int width, int height) {
  int width_plus_one = width + 1;
  int width_minus_one = width - 1;
  PIXELM * pixel_pointer = pixel + width_plus_one;
  float * WIP = wrapped + width_plus_one; //WIP is the wrapped image pointer
  float H, V, D1, D2;
  int i, j;

  for (i = 1; i < height - 1; ++i) {
    for (j = 1; j < width - 1; ++j) {
      H = wrap( * (WIP - 1) - * WIP) - wrap( * WIP - * (WIP + 1));
      V = wrap( * (WIP - width) - * WIP) - wrap( * WIP - * (WIP + width));
      D1 = wrap( * (WIP - width_plus_one) - * WIP) - wrap( * WIP - * (WIP + width_plus_one));
      D2 = wrap( * (WIP - width_minus_one) - * WIP) - wrap( * WIP - * (WIP + width_minus_one));
      pixel_pointer -> reliability *= (H * H + V * V + D1 * D1 + D2 * D2);
      pixel_pointer++;
      WIP++;
    }
    pixel_pointer += 2;
    WIP += 2;
  }
}

//calculate the reliability of the horizontal edges of the image
//it is calculated by adding the reliability of pixel and the relibility of
//its right-hand neighbour
//edge is calculated between a pixel and its next neighbour
void doEDGEs(PIXELM * pixel, EDGE * edge, int width, int height) {
  int i, j;
  EDGE * edge_pointer = edge;
  PIXELM * pixel_pointer = pixel;

  for (i = 0; i < height; i++) {
    for (j = 0; j < width - 1; j++) {
      edge_pointer -> pointer_1 = pixel_pointer;
      edge_pointer -> pointer_2 = (pixel_pointer + 1);
      edge_pointer -> reliab = pixel_pointer -> reliability + (pixel_pointer + 1) -> reliability;
      edge_pointer -> increment = find_wrap(pixel_pointer -> value, (pixel_pointer + 1) -> value);
      edge_pointer++;
      pixel_pointer++;
    }
    pixel_pointer++;
  }
  pixel_pointer=pixel;
  for (i = 0; i < height - 1; i++) {
    for (j = 0; j < width; j++) {
      edge_pointer -> pointer_1 = pixel_pointer;
      edge_pointer -> pointer_2 = (pixel_pointer + width);
      edge_pointer -> reliab = pixel_pointer -> reliability + (pixel_pointer + width) -> reliability;
      edge_pointer -> increment = find_wrap(pixel_pointer -> value, (pixel_pointer + width) -> value);
      edge_pointer++;
      pixel_pointer++;
    } //j loop
  } // i loop

}

//gather the pixels of the image into groups
void gatherPIXELs(EDGE * edge, int no_of_edges) {
  int k;
  PIXELM * PIXEL1;
  PIXELM * PIXEL2;
  PIXELM * group1;
  PIXELM * group2;
  EDGE * pointer_edge = edge;
  int increment;

  for (k = 0; k < no_of_edges; k++) {
    PIXEL1 = pointer_edge -> pointer_1;
    PIXEL2 = pointer_edge -> pointer_2;

    //PIXELM 1 and PIXELM 2 belong to different groups
    //initially each pixel is a group by it self and one pixel can construct a group
    //no else or else if to this if
    if (PIXEL2 -> head != PIXEL1 -> head) {
      //PIXELM 2 is alone in its group
      //merge this pixel with PIXELM 1 group and find the number of 2 pi to add
      //to or subtract to unwrap it
      if ((PIXEL2 -> next == NULL) && (PIXEL2 -> head == PIXEL2)) {
        PIXEL1 -> head -> last -> next = PIXEL2;
        PIXEL1 -> head -> last = PIXEL2;
        (PIXEL1 -> head -> number_of_pixels_in_group) ++;
        PIXEL2 -> head = PIXEL1 -> head;
        PIXEL2 -> increment = PIXEL1 -> increment - pointer_edge -> increment;
      }

      //PIXELM 1 is alone in its group
      //merge this pixel with PIXELM 2 group and find the number of 2 pi to add
      //to or subtract to unwrap it
      else if ((PIXEL1 -> next == NULL) && (PIXEL1 -> head == PIXEL1)) {
        PIXEL2 -> head -> last -> next = PIXEL1;
        PIXEL2 -> head -> last = PIXEL1;
        (PIXEL2 -> head -> number_of_pixels_in_group) ++;
        PIXEL1 -> head = PIXEL2 -> head;
        PIXEL1 -> increment = PIXEL2 -> increment + pointer_edge -> increment;
      }

      //PIXELM 1 and PIXELM 2 both have groups
      else {
        group1 = PIXEL1 -> head;
        group2 = PIXEL2 -> head;
        //if the no. of pixels in PIXELM 1 group is larger than the
        //no. of pixels in PIXELM 2 group.  Merge PIXELM 2 group to
        //PIXELM 1 group and find the number of wraps between PIXELM 2
        //group and PIXELM 1 group to unwrap PIXELM 2 group with respect
        //to PIXELM 1 group.  the no. of wraps will be added to PIXELM 2
        //group in the future
        if (group1 -> number_of_pixels_in_group > group2 -> number_of_pixels_in_group) {
          //merge PIXELM 2 with PIXELM 1 group
          group1 -> last -> next = group2;
          group1 -> last = group2 -> last;
          group1 -> number_of_pixels_in_group = group1 -> number_of_pixels_in_group + group2 -> number_of_pixels_in_group;
          increment = PIXEL1 -> increment - pointer_edge -> increment - PIXEL2 -> increment;
          //merge the other pixels in PIXELM 2 group to PIXELM 1 group
          while (group2 != NULL) {
            group2 -> head = group1;
            group2 -> increment += increment;
            group2 = group2 -> next;
          }
        }

        //if the no. of pixels in PIXELM 2 group is larger than the
        //no. of pixels in PIXELM 1 group.  Merge PIXELM 1 group to
        //PIXELM 2 group and find the number of wraps between PIXELM 2
        //group and PIXELM 1 group to unwrap PIXELM 1 group with respect
        //to PIXELM 2 group.  the no. of wraps will be added to PIXELM 1
        //group in the future
        else {
          //merge PIXELM 1 with PIXELM 2 group
          group2 -> last -> next = group1;
          group2 -> last = group1 -> last;
          group2 -> number_of_pixels_in_group = group2 -> number_of_pixels_in_group + group1 -> number_of_pixels_in_group;
          increment = PIXEL2 -> increment + pointer_edge -> increment - PIXEL1 -> increment;
          //merge the other pixels in PIXELM 2 group to PIXELM 1 group
          while (group1 != NULL) {
            group1 -> head = group2;
            group1 -> increment += increment;
            group1 = group1 -> next;
          } // while

        } // else
      } //else
    } //if
    pointer_edge++;
  }
}

//unwrap the image
void unwrapImage(PIXELM * pixel, float * unwrapped_image, int image_size) {
  for (int i = 0; i < image_size; i++) {
    pixel[i].value += pixel[i].increment;
  }
  for (int i = 0; i < image_size; i++) {
    unwrapped_image[i] = pixel[i].value;
  }
}

//the main function of the unwrapper
void
c_unwrap2D(float * wrapped_image, float * quality_image, float * unwrapped_image, int height, int width) {
  int image_size = height * width;
  PIXELM *pixel = (PIXELM * ) calloc(image_size, sizeof(PIXELM));
  int no_of_edges = 2 * image_size - width - height;
  EDGE *edge = (EDGE * ) calloc(no_of_edges, sizeof(EDGE));

  initialisePIXELs(wrapped_image, quality_image, pixel, width, height);
  calculate_reliability(wrapped_image, quality_image, pixel, width, height);
  doEDGEs(pixel, edge, width, height);

  //sort the EDGEs depending on their reiability. The PIXELs with higher relibility (small value) first
  quicker_sort(edge, edge + no_of_edges - 1);

  //gather PIXELs into groups
  gatherPIXELs(edge, no_of_edges);

  unwrapImage(pixel, unwrapped_image, image_size);

  free(edge);
  free(pixel);
}

py::array_t<float> unwrap2D(py::array_t<float> input1, py::array_t<float> input2) {

    py::array_t<float> input1_c = py::array_t<float,py::array::c_style| py::array::forcecast>(input1);
    py::array_t<float> input2_c = py::array_t<float,py::array::c_style| py::array::forcecast>(input2);
//     py::array_t<float> input2_c=ensure_c_style_row_major(input2);

    py::buffer_info buf1 = input1_c.request();
    py::buffer_info buf2 = input2_c.request();

    if (buf1.ndim != 2 || buf2.ndim != 2)
        throw std::runtime_error("Input should be 2-D NumPy arrays");

    if (buf1.shape[0] != buf2.shape[0] || buf1.shape[1] != buf2.shape[1])
        throw std::runtime_error("Input arrays must have the same dimensions");

//     py::array_t<float> input1_c=
    auto ptr1 = static_cast<float*>(buf1.ptr);
    auto ptr2 = static_cast<float*>(buf2.ptr);

    std::vector<float> input_vec1(ptr1, ptr1 + buf1.size);
    std::vector<float> input_vec2(ptr2, ptr2 + buf2.size);

    std::vector<float> result_vec(input_vec1.size(),0);
//     std::cout << buf1.shape[1] << "  " << buf1.shape[0] <<std::endl;
    c_unwrap2D(&input_vec1[0], &input_vec2[0], &result_vec[0], buf1.shape[0], buf1.shape[1]);


    py::array_t<float> result({buf1.shape[0], buf1.shape[1]});
    auto result_ptr = static_cast<float*>(result.request().ptr);

    std::copy(result_vec.begin(), result_vec.end(), result_ptr);

    return result;
}

PYBIND11_MODULE(pyunwrap, m) {
    m.def("unwrap2D", &unwrap2D, "Quality guided algorithm unwrap");
}
