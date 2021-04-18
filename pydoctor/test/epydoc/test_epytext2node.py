"""
Test how epytext is transformed to HTML using L{ParsedDocstring.to_node()} and L{node2stan.node2stan()} functions.
"""

from typing import List

from pydoctor.epydoc.markup import ParseError, flatten
from pydoctor.epydoc.markup.epytext import parse_docstring
from pydoctor.node2stan import node2stan
from pydoctor.test import NotFoundLinker
from pydoctor.test.epydoc.test_restructuredtext import prettify

from docutils import nodes

def epytext2node(s: str) -> nodes.document:
    errors: List[ParseError] = []
    parsed = parse_docstring(s, errors)
    assert not errors
    return parsed.to_node()

def epytext2html(s: str) -> str:
    return prettify(flatten(node2stan(epytext2node(s), NotFoundLinker())))
    
def test_epytext_paragraph() -> None:
    doc = '''
        This is a paragraph.  Paragraphs can
        span multiple lines, and can contain
        I{inline markup}.


        This is another paragraph.  Paragraphs
        are separated by blank lines.
        '''
    expected = '''
        <div class="rst-section">
         <p>
          This is a paragraph.  Paragraphs can span multiple lines, and can contain
          <em>
           inline markup
          </em>
          .
         </p>
         <p>
          This is another paragraph.  Paragraphs are separated by blank lines.
         </p>
        </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_ordered_list() -> None:
    doc = '''
          1. This is an ordered list item.

          2. This is another ordered list
          item.

          3. This is a third list item.  Note that
             the paragraph may be indented more
             than the bullet.

        This ends the list.

          4. This new list starts at four.
        '''
    expected = '''
         <div class="rst-section">
          <ol>
           <li>
            <span class="rst-first">
             This is an ordered list item.
            </span>
           </li>
           <li>
            <span class="rst-first">
             This is another ordered list item.
            </span>
           </li>
           <li>
            <span class="rst-first">
             This is a third list item.  Note that the paragraph may be indented more than the bullet.
            </span>
           </li>
          </ol>
          <p>
           This ends the list.
          </p>
          <ol>
           <li>
            <span class="rst-first">
             This new list starts at four.
            </span>
           </li>
          </ol>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_nested_list() -> None:
    doc = '''
        This is a paragraph.
            1. This is a list item.
            2. This is a second list
               item.
                 - This is a sublist.
        '''
    expected = '''
         <div class="rst-section">
          <p>
           This is a paragraph.
          </p>
          <ol>
           <li>
            <span class="rst-first">
             This is a list item.
            </span>
           </li>
           <li>
            <span class="rst-first">
             This is a second list item.
            </span>
            <ul>
             <li>
              <span class="rst-first">
               This is a sublist.
              </span>
             </li>
            </ul>
           </li>
          </ol>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_complex_list() -> None:
    doc = '''
        This is a paragraph.
          1. This is a list item.
            - This is a sublist.
            - The sublist contains two
              items.
                - The second item of the
                  sublist has its own sublist.

          2. This list item contains two
             paragraphs and a doctest block.

             >>> len('This is a doctest block')
             23

             This is the second paragraph.
        '''
    expected = '''
         <div class="rst-section">
          <p>
           This is a paragraph.
          </p>
          <ol>
           <li>
            <span class="rst-first">
             This is a list item.
            </span>
            <ul>
             <li>
              <span class="rst-first">
               This is a sublist.
              </span>
             </li>
             <li>
              <span class="rst-first">
               The sublist contains two items.
              </span>
              <ul>
               <li>
                <span class="rst-first">
                 The second item of the sublist has its own sublist.
                </span>
               </li>
              </ul>
             </li>
            </ul>
           </li>
           <li>
            <span class="rst-first">
             This list item contains two paragraphs and a doctest block.
            </span>
            <pre class="py-doctest">
<span class="py-prompt">&gt;&gt;&gt; </span><span class="py-builtin">len</span>(<span class="py-string">'This is a doctest block'</span>)
<span class="py-output">23</span>
</pre>
            <p>
             This is the second paragraph.
            </p>
           </li>
          </ol>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_sections() -> None:
    doc = '''
        This paragraph is not in any section.

        Section 1
        =========
          This is a paragraph in section 1.

          Section 1.1
          -----------
          This is a paragraph in section 1.1.

        Section 2
        =========
          This is a paragraph in section 2.
        '''
    expected = '''
         <div class="rst-section">
          <p>
           This paragraph is not in any section.
          </p>
          <div class="rst-section">
           <h2 class="heading">
            Section 1
           </h2>
           <p>
            This is a paragraph in section 1.
           </p>
           <div class="rst-section">
            <h3 class="heading">
             Section 1.1
            </h3>
            <p>
             This is a paragraph in section 1.1.
            </p>
           </div>
          </div>
          <div class="rst-section">
           <h2 class="heading">
            Section 2
           </h2>
           <p>
            This is a paragraph in section 2.
           </p>
          </div>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_literal_block() -> None:
    doc = '''
        The following is a literal block::

            Literal /
                   / Block

        This is a paragraph following the
        literal block.
        '''
    expected = '''
        <div class="rst-section">
          <p>
           The following is a literal block:
          </p>
          <pre class="rst-literal-block">
    Literal /
           / Block
</pre>
          <p>
           This is a paragraph following the literal block.
          </p>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_inline() -> None:
    doc = '''
        I{B{Inline markup} may be nested; and
        it may span} multiple lines.

          - I{Italicized text}
          - B{Bold-faced text}
          - C{Source code}
          - Math: M{m*x+b}

        Without the capital letter, matching
        braces are not interpreted as markup:
        C{my_dict={1:2, 3:4}}.
        '''
    expected = '''
         <div class="rst-section">
          <p>
           <em>
            <strong>
             Inline markup
            </strong>
            may be nested; and it may span
           </em>
           multiple lines.
          </p>
          <ul>
           <li>
            <span class="rst-first">
             <em>
              Italicized text
             </em>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <strong>
              Bold-faced text
             </strong>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <tt class="rst-docutils literal">
              Source code
             </tt>
            </span>
           </li>
           <li>
            <span class="rst-first">
             Math:
             <span class="rst-math rst-formula">
              <i>
               m
              </i>
              *
              <i>
               x
              </i>
              +
              <i>
               b
              </i>
             </span>
            </span>
           </li>
          </ul>
          <p>
           Without the capital letter, matching braces are not interpreted as markup:
           <tt class="rst-docutils literal">
            <span class="pre">
             my_dict={1:2,
            </span>
            3:4}
           </tt>
           .
          </p>
         </div>
        '''
    assert epytext2html(doc) == prettify(expected)
    

def test_epytext_url() -> None:
    doc = '''
        - U{www.python.org}
        - U{http://www.python.org}
        - U{The epydoc homepage<http://
          epydoc.sourceforge.net>}
        - U{The B{I{Python}} homepage
          <www.python.org>}
        - U{Edward Loper<mailto:edloper@
          gradient.cis.upenn.edu>}
        '''
    expected = '''
        <div class="rst-section">
          <ul>
           <li>
            <span class="rst-first">
             <a class="rst-reference external" href="http://www.python.org" target="_top">
              www.python.org
             </a>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <a class="rst-reference external" href="http://www.python.org" target="_top">
              http://www.python.org
             </a>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <a class="rst-reference external" href="http://epydoc.sourceforge.net" target="_top">
              The epydoc homepage
             </a>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <a class="rst-reference external" href="&lt;strong&gt;&lt;emphasis&gt;Python&lt;/emphasis&gt;&lt;/strong&gt;" target="_top">
              The
             </a>
            </span>
           </li>
           <li>
            <span class="rst-first">
             <a class="rst-reference external" href="mailto:edloper@gradient.cis.upenn.edu" target="_top">
              Edward Loper
             </a>
            </span>
           </li>
          </ul>
         </div>
        '''

    assert epytext2html(doc) == prettify(expected)

def test_epytext_symbol() -> None:
    doc = '''
        Symbols can be used in equations:
          - S{sum}S{alpha}/x S{<=} S{beta}

        S{<-} and S{larr} both give left
        arrows.  Some other arrows are
        S{rarr}, S{uarr}, and S{darr}.
        '''
    expected = '''
        <div class="rst-section">
        <p>Symbols can be used in equations:</p>
        <ul>
            <li><span class="rst-first"><span>&#8721;</span><span>&#945;</span>/x <span>&#8804;</span> <span>&#946;</span></span></li>
        </ul>
        <p><span>&#8592;</span> and <span>&#8592</span> both give left arrows.  Some other arrows are <span>&#8594;</span>, <span>&#8593;</span>, and <span>&#8595;</span>.</p>
        </div>
        '''
    assert epytext2html(doc) == prettify(expected)
