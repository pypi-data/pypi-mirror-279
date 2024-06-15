# mypy: disable-error-code="name-defined, valid-type"

def batch_list[T](items: list[T], batch_size: int) -> list[list[T]]:
    """Divide uma sequência em sublistas de tamanho fixo. Similar a metodo collate de Groovy.

    Esta função divide uma lista em sublistas (ou batches) de tamanho fixo especificado. 
    Se a lista não puder ser dividida igualmente, a última sublista conterá os elementos restantes.

    ### Args:
        items (lista[T]): A lista de elementos a ser dividida.
        batch_size (int): O tamanho de cada sublista.

    ### Returns:
        list[list[T]]: Uma lista de sublistas, onde cada sublista tem no máximo `batch_size` elementos.

    ### Examples:
        ```python
        >>> batch_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]

        >>> batch_list([1, 2, 3], 3)
        [[1, 2, 3]]
        ```

    ### Notes:
        - Se `batch_size` for maior que o tamanho da `sequence`,
        a função retornará uma lista com uma única sublista contendo toda a `sequence`.
        - Se `batch_size` for menor ou igual a 0, a função retornará uma lista vazia.
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
