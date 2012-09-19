#/usr/bin/make -f

.PHONY : all clean rebuild

PDFDIR=pdf
IMGDIR=images
SOURCES=sources

PDFS:=$(patsubst $(SOURCES)/%.tex, $(PDFDIR)/%.pdf, $(wildcard $(SOURCES)/*.tex))
IMG_PDFS:=$(patsubst %.svg, %.pdf, $(wildcard $(IMGDIR)/*.svg))

ifdef NO_BATCH
	BATCH:=
else
    BATCH:=-interaction=batchmode
endif

all: $(IMG_PDFS) $(PDFS)

$(PDFDIR)/%.pdf:$(SOURCES)/%.tex files/lectures_env.tex files/python_cmds.tex 
		xelatex $(BATCH) -output-directory=$(PDFDIR) $<
		-bash -c 'cd $(PDFDIR) && rm `ls -1 | grep -v ".pdf"`'

$(IMGDIR)/%.pdf:$(IMGDIR)/%.svg
		rsvg-convert -f pdf -o $@ $^

clean:
		-rm pdf/* $(IMG_PDFS)

rebuild: clean all
