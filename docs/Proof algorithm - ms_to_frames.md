# ms_to_frames - Explanation

To convert an frame to an ms, here is the formula: $$ms = round(frame * {denominator \over numerator})$$

Important to note, here the rounding method round up, so, if it encounter $round(x.5)$, it will become $x + 1$

From the previous equation, we can deduce this:
$$ms - 0.5 \le frame * {denominator \over numerator} < ms + 0.5$$

And from the previous inequation, we can isolate $frame$ like this:
$$(ms - 0.5) * {numerator \over denominator} \le frame < (ms + 0.5) * {numerator \over denominator}$$

But, don't forget, $frame \in \mathbb{N}$. This means we need to take the **integer** between the 2 bounds.

If there is no integer, this means that the 2 bounds are the same frame, so we can take one of the 2 bounds and floor it.

## Example of frame corresponding ms
```math
\begin{gather}
fps = 24000/1001 \\
Frame_0 : [0, 42[ ms \\
Frame_1 : [42, 83[ ms \\
Frame_2 : [83, 125[ ms \\
Frame_3 : [125, 167[ ms
\end{gather}
```

## Example where the 2 bounds are the same frame
```math
\begin{gather}
ms = 82 \\
numerator = 24000/1001 \\
denominator = 1000 \\
1.95404 \le frame < 1.97802
\end{gather}
```
So, for $ms = 82$, the $frame = 1$

## Example where the 2 bounds aren't the same frame
```math
\begin{gather}
ms = 83 \\
numerator = 24000/1001 \\
denominator = 1000 \\
1.97802 \le frame < 2.002
\end{gather}
```
So, for $ms = 83$, the $frame = 2$

We need an algorithm to do that.
There is probably many ways how to do that, but here is what i think is the easiest:
```py
# We use the upper bound
upper_bound = (ms + 0.5) * numerator / denominator
# Then, we trunc the result
trunc_frame = int(upper_bound)

# If the upper_bound equals to the trunc_frame, this means that we don't respect the inequation because it is "greater than", not "greater than or equals".
# So if it happens, this means we need to return the previous frame
if upper_bound == trunc_frame:
    return trunc_frame - 1
else:
    return trunc_frame
```
