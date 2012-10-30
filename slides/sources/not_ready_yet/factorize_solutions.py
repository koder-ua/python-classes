%-------------------------------------------------------------------------------
{\center Прошлое задание}
\begin{lstlisting}
    def factorize(val):
        result = []
        for possible_divider in range(2, val):
            while val % possible_divider == 0:
                result.append(possible_divider)
                val /= possible_divider

        return result
\end{lstlisting}
\newpage

%-------------------------------------------------------------------------------
{\center Прошлое задание 2}
\begin{lstlisting}
    def factorize(val):
        result = []
        for possible_divider in xrange(2, int(val ** 0.5) + 1):
            while val % possible_divider == 0:
                result.append(possible_divider)
                val /= possible_divider

        if 1 != val:
            result.append(val)

        return result
\end{lstlisting}
\newpage

%-------------------------------------------------------------------------------
{\center Прошлое задание 4}
\begin{lstlisting}
    def factorize(val):
        result = []

        while val % 2 == 0:
            result.append(2)
            val /= 2

        for possible_divider in xrange(3, int(val ** 0.5) + 1, 2):
            while val % possible_divider == 0:
                result.append(possible_divider)
                val /= possible_divider

        if 1 != val:
            result.append(val)

        return result
\end{lstlisting}
\newpage

%-------------------------------------------------------------------------------
{\center Прошлое задание 3}
\begin{lstlisting}
    def factorize(val):
        for possible_divider in xrange(2, int(val ** 0.5) + 1):
            while val % possible_divider == 0:
                yield possible_divider
                val /= possible_divider

        if 1 != val:
            yield val
\end{lstlisting}
\newpage

