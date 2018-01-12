---
layout: post
comments: true
title: "Core Topological Data Analysis"
subtitle: "The Mapper Algorithm"
tags: [tda, topological data analysis, mapper, Ayasdi, graph, data visualization, data reduction, clustering]
author: "Mike"
---
In this post we are going to get an overview of the mapper algorithm.  Mapper is
one of the main algorithms used in topological data analysis and it is the core of the multi-million dollar company [Ayasdi](https://www.ayasdi.com).  

Mapper is a local clustering algorithm that produces a compact and easily visualized view of a (potentially large) data set <!--more-->. It produces a graph of vertices and edges which can visually summarize trends or highlight interesting subsets of the data. It can be combined with machine learning or other statistical techniques and it has some nice mathematical guarantees (under the right assumptions) on it ability to preserve the shape of the data.

The best part of the mapper algorithm is its simplicity. The basic idea is to cluster the data in small chunks and then 'glue those chunks together' to get a low dimensional visual summary of the data.  The clustering can be done using any clustering algorithm and any notion of distance or similarity between points which makes it very flexible.  

##### Nuts and Bolts
To understand how the mapper algorithm works we need to be comfortable with the [inverse image of a function](https://en.wikipedia.org/wiki/Image_(mathematics)#Inverse_image). An example will hopefully suffice for those that need a reminder: let $f(x) = \sqrt{x}$ then $f^{-1}((3,4)) = (9,16)$ since the numbers the interval (9,16) maps to (3,4) under the square root function.  

Lets assume we have a data set, $D$. The mapper algorithm is summarized as follows.
1. Define a function $f:D\to \mathbb{R}$ on our data set.  The function is arbitrary but its choice is important and different choices will result in different outputs.
2. Build a graph from the Data:  
    *  Breaking up the real line into overlapping intervals $(a_1, b_1), (a_2,b_2), \ldots (a_n, b_n)$  
    *  For each interval cluster the points of $f^{-1}(a_i, b_i)$  using your favorite clustering algorithm  
    *  Build a graph such that each vertex corresponds to exactly one cluster from the last step  
    *  Draw an edge between vertices if the clusters have any points in common.  For example this happens when $f^{-1}(a_i,b_i)\cap f^{-1}(a_j,b_j) \neq ∅$. Since we assumed the intervals are overlapping this happens often.

3. Optional: Color and size the nodes of the graph by features of the data. For example one can size the nodes of the graph by the number of points in the cluster corresponding to that node and color it by the average value of the function on the points in the cluster.

##### Example
Lets take a look at a simple example which illustrates the process.  Imagine we have sampled data from a circle:

![Mapper Circle]({{ site.baseurl}}/assets/posts/2018-01-01-mapper-circle.png)

For our function we choose to map each point to its height i.e. $f(x,y) = y.$  

![Mapper Function]({{site.baseurl}}/assets/posts/2018-01-01-mapper2.png)


For simplicity suppose the highest point is at height 1 and lowest point has height -1.  We can choose $[-1,-\frac{1}{4}],[-\frac{1}{2},\frac{1}{2}],[\frac{1}{4},1]$ as our intervals.  There is no particular reason for this choice other than the intervals overlap and they cover the image of $f.$

![Mapper Overlap]({{site.baseurl}}/assets/posts/2018-01-01-mapper-inverse-image.png)

We need to cluster the sets $f^{-1}(a_i,b_i)$ by any clustering algorithm and build a graph with one vertex per cluster.  For this post I will be using the cluster-by-visual-inspection algorithm.  The points of $f^{-1}([-1,-\frac{1}{4}])$ all seem to be one cluster so I add one vertex to the graph for this cluster.  The points in $f^{-1}([-\frac{1}{2},\frac{1}{2}])$ seem to form 2 distinct clusters so I will add two vertices to the graph, one for each cluster.  Finally $f^{-1}([\frac{1}{4},1])$ seems to be again one cluster so I add a final vertex to the graph.  If we layout the vertices in a similar arrangement to where they came from in the original data we have the following graph:

![Mapper Graph Without Edges]({{site.baseurl}}/assets/posts/2018-01-01-mapper-graph-no-edges.png)

The only thing left to do is determine the edges between the vertices.  Each vertex is associated to a local cluster and there is an edge between vertices if the clusters have any points in common.  Therefore we get the final representation:

![Mapper Graph With Edges]({{site.baseurl}}/assets/posts/2018-01-01-mapper-graph-edges.png)

We have reduced our noisy circle to a simple graph, 4 data points with 4 edges. Even better is that the graph is topologically equivalent to a circle so we have retained the overall 'shape' of the data.  We could have chosen to color or size to nodes to add to the visual information present in the graph but I didn't do that here.

If you understand this example then you understand the basic idea behind mapper.  Come up with some examples on your own or go read the [original paper]((http://cs233.stanford.edu/ReferencedPapers/mapperPBG.pdf)).  In a future post we will discuss more example, and how mapper and machine learning can be combined.
