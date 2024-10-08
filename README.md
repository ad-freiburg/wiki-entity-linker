# Wiki Entity Linker

The Wiki Entity Linker is a tool for entity linking and coreference resolution on Wikipedia.
The Wiki Entity Linker utilizes intra-Wikipedia hyperlinks to produce high-quality entity linking results.

The code is based on [ELEVANT](https://github.com/ad-freiburg/elevant), a tool for evaluating, analyzing and
 comparing entity linking systems. This way, the Wiki Entity Linker can be easily evaluated.

We summarized the most important information and instructions about how to use the Wiki Entity Linker in this README.
For further information, particularly regarding the evaluation of the linker, please check the
[ELEVANT Wiki](https://github.com/ad-freiburg/elevant/wiki).


## Docker Instructions
Get the code, and build and start the docker container:

    git clone https://github.com/ad-freiburg/wiki_entity_linker.git .
    docker build -t wiki_entity_linker .
    docker run -it -p 8000:8000 \
        -v <data_directory>:/data \
        -v $(pwd)/evaluation-results/:/home/evaluation-results \
        -v $(pwd)/benchmarks/:/home/benchmarks \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v $(pwd)/wikidata-types/:/home/wikidata-types \
        -e WIKIDATA_TYPES_PATH=$(pwd) wiki_entity_linker

where `<data_directory>` is the directory in which the required data files will be stored. What these data files are
 and how they are generated is explained in section [Get the Data](#get-the-data). Make sure you can read from and
 write to all directories that are being mounted as volumes from within the docker container (i.e. your
 `<data_directory>`, `evaluation-results` and `benchmarks`), for example (if security is not an issue) by giving all
 users read and write permissions to the directories in question with:

    chmod a+rw -R <data_directory> evaluation-results/ benchmarks/ wikidata-types/


All the following commands should be run inside the docker container.


## Get the Data
For linking entities in text or evaluating the output of a linker, our system needs information about entities and
 mention texts, e.g. entity names, aliases, popularity scores, types, the frequency with which a mention is linked
 to a certain article in Wikipedia, etc. This information is stored in and read from several files. Since these files
 are too large to upload them on GitHub, you can either download them from our servers (fast) or build them yourself
 (slow, RAM intensive, but the resulting files will be based on recent Wikidata and Wikipedia dumps).

To download the files from our servers, simply run

    make download_all

This will automatically run `make download_wikidata_mappings`, `make download_wikipedia_mappings` and
 `make download_entity_types_mapping` which will download the compressed files, extract them and move them to the
 correct location. See [Mapping Files](https://github.com/ad-freiburg/elevant/wiki/Mapping-Files) for a description of files downloaded in these steps.

NOTE: This will overwrite existing Wikidata and Wikipedia mappings in your `<data_directory>` so make sure this is what 
 you want to do.

If you rather want to build the mappings yourself, you can run `make generate_all` to generate all required files, or
 alternatively, replace only a specific *download* command by the corresponding *generate* command.
See [Data Generation](https://github.com/ad-freiburg/elevant/wiki/Generating-Data) for more details.

## Link Wikipedia Dump
If you want to use the Wiki Entity Linker to link an entire Wikipedia dump, follow these steps:
1) First download and extract a Wikipedia dump by running

       make download_wiki extract_wiki
        
    NOTE: If you built the Wikipedia mappings yourself instead of downloading them from our servers, then a Wikipedia
     dump was already downloaded and extracted, so you can skip this step. Unless you want to link a more recent dump
     than the one you downloaded for the Wikipedia mapping generation. In that case make sure your existing Wikipedia
     dump files are not being overwritten by either renaming your existing
     `<data_directory>/wikipedia_dump_files/enwiki-latest-pages-articles-multistream.xml.bz2` and
     `<data_directory>/wikipedia_dump_files/enwiki-latest-extracted.jsonl` files or by adjusting the `WIKI_DUMP` and
     `EXTRACTED_WIKI_DUMP` variables in the Makefile.

2) To link the downloaded Wikipedia dump using our best system run
    
       make link_wiki
    
This uses our hyperlink-reference linker which links entities based on intra-Wikipedia hyperlinks, our popular-entities
 linker which links remaining entities based on their Wikidata sitelink count with special rules for demonyms,
 and our coreference linker which uses type and gender information of previously linked entities and dependency parse
 information to resolve coreferences.

NOTE: Linking the entire Wikipedia dump will take several hours.
You can adjust the number of processes used for linking via the Makefile variable `NUM_LINKER_PROCESSES`.

The output file (per default `<data_directory>/wikipedia_dump_files/enwiki-latest-linked.jsonl`)
will contain one json object representing a linked Wikipedia article per line.

### Create QLever Text Files
If you want to use the linked Wikipedia dump for full-text search in QLever as described
[here](https://github.com/ad-freiburg/qlever/blob/master/docs/sparql_plus_text.md) run

    python3 create_qlever_text_files.py <input_file> <output_prefix>

where `<input_file>` is the linked Wikipedia dump file
(usually `<data_directory>/wikipedia_dump_files/enwiki-latest-linked.jsonl`)
and `<output_prefix>` is the prefix for the generated output files.
This will generate two files `<output_prefix>.wordsfile.tsv` and `<output_prefix>.docsfile.tsv`
which can then be used as input for a SPARQL + Text instance of QLever.

## Evaluation
To evaluate the Wiki Entity Linker, you can use the ELEVANT evaluation web app, which is included in this repository.

1) First, link the benchmark articles with the Wiki Entity Linker. For this, you can use the script `link_benchmark.py`.
 For example,

       python3 link_benchmark.py "Wiki Entity Linker" -l popular-entities -hl hyperlink-reference -coref entity -b wiki-fair-v2-dev wiki-fair-v2-test

   will run the Wiki Entity Linker over the Wiki-Fair v2.0 development and test sets. This will create the file
    `evaluation-results/popular-entities/wiki_entity_linker.wiki-fair-v2-dev.linked_articles.jsonl` for the linked
    development set and a similar file for the linked test set. The result files contains one article as JSON object per
    line. Each JSON object contains benchmark article information such as the article title, text, and ground truth
    labels, as well as the entity mentions produced by the linker.

2) Evaluate the linking results. For this, you can use the script `evaluate.py`. For example,

       python3 evaluate.py evaluation-results/popular-entities/wiki_entity_linker.wiki-fair-v2-*.linked_articles.jsonl

   will evaluate the linking results for the previously linked Wiki-Fair v2.0 development and test sets, print
   precision, recall and F1 scores and create two new files that contain information about the evaluation results
   which will be read by the evaluation web app.

3) Start the evaluation web app by running

       make start_webapp

   You can then access the webapp at <http://0.0.0.0:8000/> and inspect the evaluation results.

For more information about the evaluation process, including instructions for how to add your own benchmark, and
 details on the web app's features, please refer to the [ELEVANT Wiki](https://github.com/ad-freiburg/elevant/wiki).
