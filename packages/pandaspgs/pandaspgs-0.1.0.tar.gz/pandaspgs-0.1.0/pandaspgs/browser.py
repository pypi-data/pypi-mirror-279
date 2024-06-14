import webbrowser


def open_score_in_pgs_catalog(pgs_id: str) -> bool:
    """
    This function launches the web browser and opens a tab for each identifier on the PGS Catalog web graphical user interface: https://www.pgscatalog.org/.

    Args:
        pgs_id: This argument indicates the type of the identifiers passed in identifier

    Returns:
        Returns TRUE if successful, or FALSE otherwise. But note that this function is run for its side effect.
    ```python
    from pandaspgs.browser import open_score_in_pgs_catalog
    open_score_in_pgs_catalog('PGS000001')
    ```

    """
    return webbrowser.open_new_tab('https://www.pgscatalog.org/score/%s' % pgs_id)


def open_publication_in_pgs_catalog(pgp_id: str) -> bool:
    """
    This function launches the web browser and opens a tab for each identifier on the PGS Catalog web graphical user interface: https://www.pgscatalog.org/.

    Args:
        pgp_id: This argument indicates the type of the identifiers passed in identifier

    Returns:
        Returns TRUE if successful, or FALSE otherwise. But note that this function is run for its side effect.
    ```python
    from pandaspgs.browser import open_publication_in_pgs_catalog
    open_publication_in_pgs_catalog('PGP000001')
    ```

    """
    return webbrowser.open_new_tab('https://www.pgscatalog.org/publication/%s' % pgp_id)


def open_sample_set_in_pgs_catalog(pss_id: str) -> bool:
    """
    This function launches the web browser and opens a tab for each identifier on the PGS Catalog web graphical user interface: https://www.pgscatalog.org/.

    Args:
        pss_id: This argument indicates the type of the identifiers passed in identifier

    Returns:
        Returns TRUE if successful, or FALSE otherwise. But note that this function is run for its side effect.
    ```python
    from pandaspgs.browser import open_sample_set_in_pgs_catalog
    open_sample_set_in_pgs_catalog('PSS000001')
    ```

    """
    return webbrowser.open_new_tab('https://www.pgscatalog.org/sampleset/%s' % pss_id)


def open_trait_in_pgs_catalog(efo_id: str) -> bool:
    """
    This function launches the web browser and opens a tab for each identifier on the PGS Catalog web graphical user interface: https://www.pgscatalog.org/.

    Args:
        efo_id: This argument indicates the type of the identifiers passed in identifier

    Returns:
        Returns TRUE if successful, or FALSE otherwise. But note that this function is run for its side effect.
    ```python
    from pandaspgs.browser import open_trait_in_pgs_catalog
    open_trait_in_pgs_catalog('EFO_0001645')
    ```

    """
    return webbrowser.open_new_tab('https://www.pgscatalog.org/trait/%s' % efo_id)


def open_in_pubmed(pubmed_id: str) -> bool:
    """
    This function launches the web browser and opens a tab for each PubMed citation.

    Args:
        pubmed_id: A PubMed identifier, either a character or an integer vector.

    Returns:
        Returns TRUE if successful. Note however that this function is run for its side effect
    ```python
    from pandaspgs.browser import open_in_pubmed
    open_in_pubmed('26301688')
    ```

    """
    return webbrowser.open_new_tab('https://www.ncbi.nlm.nih.gov/pubmed/%s' % pubmed_id)


def open_in_dbsnp(variant_id: str) -> bool:
    """
    This function launches the web browser at dbSNP and opens a tab for each SNP identifier.

    Args:
        variant_id: A variant identifier, a character vector.

    Returns:
        Returns TRUE if successful. Note however that this function is run for its side effect.
    ```python
    from pandaspgs.browser import open_in_dbsnp
    open_in_dbsnp('rs56261590')
    ```

    """
    return webbrowser.open_new_tab('https://www.ncbi.nlm.nih.gov/snp/%s' % variant_id)
