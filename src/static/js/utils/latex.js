export class LatexUtils {
    /**
     * Cleans a LaTeX string by removing extra backslashes from escaped characters.
     * Specifically, it replaces `\\`, `\{`, and `\}` with `\`, `{`, and `}` respectively.
     *
     * @param {string} latexString - The LaTeX string to clean.
     * @returns {string} The cleaned LaTeX string.
     */
    static cleanLatex(latexString) {
        if (typeof latexString !== 'string') {
            return latexString;
        }
        return latexString
            .replace(/\\\\/g, '\\') // Replace \\ with \
            .replace(/\\{/g, '{') // Replace \{ with {
            .replace(/\\}/g, '}'); // Replace \} with }
    }
}