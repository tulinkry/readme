#ifndef _bazzinga_
#define _bazzinga_

/** README
 * This is a class for everything
 * One two three
 * SECTION:
 *	there you can see section 1
 *	aweaksdlasjdlalajdljdlsdjlsjdl
 *	lskdjldfjgflksjflkdfjfdljlf
 *	SUBSECTION:
 *		it has also a subsection if you know
 *		@your mather
 *		SUBSUBSECTION:
 *			@your mother
 *			@his mother
 *			@both of us mother
 *			nejaky text
 *		SUB:
 *			opet nekytest
 *	SUBSUB:
 *		Hovna na podlaze
 * @section Hovno
 * @marketa Veverková
 */


class CArray 
{
	private:
		int * m_array;
		int m_size;
		int m_count;
	public:
				CArray ( int size );
				~CArray (void);
		bool	fill (void);
		int 	get ( int index ) const;
		bool 	set ( int index, int value );
		int 	getSize (void);
		void	print (void);
		void	sort (void);
};

#endif