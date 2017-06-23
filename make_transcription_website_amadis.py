import codecs
import os

output_dir = "/Users/dhg/workspace/amadis/output/train_output_20/finalTranscriptions"
github_dir = "/Users/dhg/workspace/halperta/amadis"
website = "http://www.halperta.com/amadis"
transcriptions_dir = "%s/transcriptions" % (github_dir)
image_dir = "%s/img"
website_image_size = "800"  # 400, 800, 1000



all_pages = dict()  # all_pages[book_name] = page_names

with codecs.open("%s/index.html" % (github_dir), 'w', encoding='utf8') as index_fout:
  index_fout.write("""
    These transcriptions were produced automatically using Ocular, with 20 training pages and 5 iterations. The system was set to expect latin and spanish. Common mistakes it makes include: S in place of Z; i in place of r; ii in place of n; b in place of d; t in place of x.\n""")
  index_fout.write("""
   For more information about these results, contact <a href="http://www.halperta.com">Hannah Alpert-Abrams</a> (halperta@gmail.com).
    <br/><br/>\n""")
  index_fout.write('<br/><br/>\n')

  if not os.path.exists("%s" % (transcriptions_dir)):
    os.makedirs("%s" % (transcriptions_dir))
  for book_name in os.listdir(output_dir):
    if book_name[0] != '.':  # skip hidden files
      if book_name not in all_pages:
        all_pages[book_name] = []
      if not os.path.exists("%s/%s" % (transcriptions_dir, book_name)):
        os.makedirs("%s/%s" % (transcriptions_dir, book_name))
      book_dir = '%s/%s/all_transcriptions/' % (output_dir, book_name)
      for filename in os.listdir(book_dir):
        # pl_blac_012_00019-1000_iter-3_transcription_normalized.txt
        suffix = "_iter-5_transcription.txt"
        if filename.endswith(suffix):
          page_name = filename[:-len(suffix)]
          all_pages[book_name].append(page_name)
      for (i, page_name) in enumerate(all_pages[book_name]):
        print('Writing %s/%s/%s.html' % (transcriptions_dir, book_name, page_name))
        with codecs.open("%s/%s/%s.html" % (transcriptions_dir, book_name, page_name), 'w', encoding='utf8') as fout:
          if i > 0:
            fout.write('<a href="%s.html">Prev</a>&nbsp;\n' % (all_pages[book_name][i-1]))
          fout.write('<a href="index.html">Up</a>&nbsp;\n' % ())
          if i < len(all_pages[book_name])-1:
            fout.write('<a href="%s.html">Next</a>\n' % (all_pages[book_name][i+1]))
          fout.write('<br/>\n')

          fout.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
          fout.write('<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/></head>\n')
          fout.write('<body>\n')
          fout.write('<table><tr><td>\n')
          with codecs.open("%s/%s%s" % (book_dir, page_name, suffix), 'r', encoding='utf8') as fin:
            for line in fin:
              fout.write("%s<br/>\n" % (line.strip()))
          fout.write('</td><td>\n')
          fout.write('<img src="http://halperta.com/amadis/img/%s/-line_extract.png">\n' % (page_name))
          fout.write('</td></tr></table>\n')
          fout.write('</body>\n')
          fout.write('</html>\n')
      with codecs.open("%s/%s/index.html" % (transcriptions_dir, book_name), 'w', encoding='utf8') as fout:
        fout.write('<a href="../../index.html">Home</a><br/><br/>\n' % ())
        for page_name in all_pages[book_name]:
          fout.write('<a href="%s.html">%s</a><br/>\n' % (page_name, page_name))
      index_fout.write('<a href="transcriptions/%s/index.html">%s</a><br/>\n' % (book_name, book_name))


