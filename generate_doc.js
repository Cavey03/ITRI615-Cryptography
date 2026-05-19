const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, PageOrientation, BorderStyle, LevelFormat,
  TabStopType, TabStopPosition, PageBreak
} = require('docx');

function readCode(file) {
  return fs.readFileSync(path.join(__dirname, 'ciphers', file), 'utf8');
}

const CODE = {
  substitution: readCode('substitution.py'),
  vigenere: readCode('vigenere.py'),
  transposition: readCode('transposition.py'),
  vernam: readCode('vernam.py'),
  caesar: readCode('caesar.py'),
};

const ARIAL = "Arial";
const MONO = "Consolas";

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    ...opts,
    children: [new TextRun({ text, font: ARIAL, size: 22 })],
  });
}

function pRuns(runs, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    ...opts,
    children: runs,
  });
}

function r(text, extra = {}) {
  return new TextRun({ text, font: ARIAL, size: 22, ...extra });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, font: ARIAL, size: 36, bold: true })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140 },
    children: [new TextRun({ text, font: ARIAL, size: 28, bold: true })],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, font: ARIAL, size: 24, bold: true })],
  });
}

function codeBlock(code) {
  const lines = code.replace(/\r\n/g, '\n').split('\n');
  return lines.map((line, i) => new Paragraph({
    spacing: { after: 0, line: 240 },
    shading: { fill: "F2F2F2", type: "clear" },
    border: i === 0
      ? { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
          left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
          right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } }
      : i === lines.length - 1
      ? { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
          left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
          right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } }
      : { left: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" },
          right: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" } },
    children: [new TextRun({ text: line || " ", font: MONO, size: 18 })],
  }));
}

function exampleBlock(lines) {
  return lines.map(line => new Paragraph({
    spacing: { after: 0, line: 240 },
    shading: { fill: "FFF8E1", type: "clear" },
    children: [new TextRun({ text: line || " ", font: MONO, size: 20 })],
  }));
}

function bullet(text) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text, font: ARIAL, size: 22 })],
  });
}

// ── Title page ────────────────────────────────────────────────────────────
const titlePage = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 2400, after: 200 },
    children: [new TextRun({
      text: "Classical Cryptography Tool",
      font: ARIAL, size: 56, bold: true,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({
      text: "Cipher Reference & Implementation",
      font: ARIAL, size: 32, color: "555555",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 600, after: 100 },
    children: [new TextRun({ text: "ITRI 615 — 2026", font: ARIAL, size: 26 })],
  }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ── Introduction ──────────────────────────────────────────────────────────
const intro = [
  h1("Overview"),
  p("This document describes the five classical ciphers implemented in the project, with a worked example and the complete Python source for each one. The ciphers covered are:"),
  bullet("Simple Substitution — keyword-based alphabet swap"),
  bullet("Vigenère — keyword-based polyalphabetic shift"),
  bullet("Transposition — columnar reordering of letters"),
  bullet("Vernam — byte-level XOR cipher (handles binary files)"),
  bullet("Caesar — single-shift monoalphabetic cipher"),
  new Paragraph({ children: [new PageBreak()] }),
];

// ── Cipher sections ───────────────────────────────────────────────────────

function section(title, paragraphs) {
  return [h1(title), ...paragraphs, new Paragraph({ children: [new PageBreak()] })];
}

const substitutionSection = section("1. Simple Substitution Cipher", [
  h2("How it works"),
  p("The user picks a keyword. A new cipher alphabet is built by writing the unique letters of the keyword first, then filling in the remaining letters of the alphabet in their normal order. Every plaintext letter is then replaced with the letter directly beneath it in this new alphabet."),
  p("Spaces, punctuation, and digits pass through unchanged. Case is preserved."),

  h2("Worked example"),
  p("Key: ZEBRA"),
  p("Building the cipher alphabet:"),
  ...exampleBlock([
    "Normal:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",
    "Cipher:  Z E B R A C D F G H I J K L M N O P Q S T U V W X Y",
  ]),
  p("Encrypting HELLO WORLD:"),
  ...exampleBlock([
    "H -> F    W -> V",
    "E -> A    O -> M",
    "L -> J    R -> P",
    "L -> J    L -> J",
    "O -> M    D -> R",
    "",
    "Result: FAJJM VMPJR",
  ]),

  h2("Code — ciphers/substitution.py"),
  ...codeBlock(CODE.substitution),
]);

const vigenereSection = section("2. Vigenère Cipher", [
  h2("How it works"),
  p("The Vigenère cipher applies multiple Caesar shifts in sequence — one for each letter of the key. The key is repeated across the plaintext, and each plaintext letter is shifted forward by the alphabet position of the matching key letter (A=0, B=1, … Z=25)."),
  p("Non-letters pass through and do not consume a key letter. The key is cleaned to keep only letters, and case is ignored when reading the key."),

  h2("Worked example"),
  p("Key: KEY    Plaintext: HELLO"),
  ...exampleBlock([
    "Plaintext:   H  E  L  L  O",
    "Key (cycle): K  E  Y  K  E",
    "Shift by:   10  4 24 10  4",
    "Cipher:      R  I  J  V  S",
    "",
    "Result: RIJVS",
  ]),
  p("Trace of H: position 7, shifted by K (10) → (7 + 10) mod 26 = 17 → R."),

  h2("Code — ciphers/vigenere.py"),
  ...codeBlock(CODE.vigenere),
]);

const transpositionSection = section("3. Transposition Cipher (Columnar)", [
  h2("How it works"),
  p("Transposition reorders letters rather than replacing them. The plaintext is written row-by-row into a grid whose width equals the key length, padded with X if the last row is incomplete. The key letters are then sorted alphabetically — that sort order determines the order in which columns are read out to form the ciphertext."),
  p("Decryption reverses the process: the grid dimensions are computed from the ciphertext length, columns are filled back in sorted order, and the rows are read left-to-right."),

  h2("Worked example"),
  p("Key: CAB    Plaintext: HELLO"),
  p("Write into a 3-column grid (padded with X):"),
  ...exampleBlock([
    "C  A  B",
    "-------",
    "H  E  L",
    "L  O  X",
  ]),
  p("Sort the key letters to find the read order:"),
  ...exampleBlock([
    "Letter:  C  A  B",
    "Col #:   0  1  2",
    "Sorted:  A(1)  B(2)  C(0)",
  ]),
  p("Read columns in sorted order:"),
  ...exampleBlock([
    "Col 1 (A): E, O  -> EO",
    "Col 2 (B): L, X  -> LX",
    "Col 0 (C): H, L  -> HL",
    "",
    "Result: EOLXHL",
  ]),

  h2("Code — ciphers/transposition.py"),
  ...codeBlock(CODE.transposition),
]);

const vernamSection = section("4. Vernam Cipher (XOR)", [
  h2("How it works"),
  p("The Vernam cipher operates on raw bytes instead of letters. The plaintext is encoded to UTF-8 bytes, the key is repeated to match the plaintext length, and each plaintext byte is XORed with the matching key byte. The result is returned as a hexadecimal string."),
  p("Because XOR is its own inverse — (A XOR K) XOR K = A — encryption and decryption use the same operation. This is the only cipher in the project that handles binary files (images, PDFs, etc.) safely, via the encrypt_bytes / decrypt_bytes helpers."),
  p("Note: this is technically a repeating-key XOR cipher, not a true one-time pad. A true Vernam cipher requires a random key as long as the message, used only once."),

  h2("Worked example"),
  p("Key: K    Plaintext: HI"),
  ...exampleBlock([
    "Plaintext:  H        I",
    "Hex:        0x48     0x49",
    "Binary:     01001000 01001001",
    "",
    "Key:        K        K",
    "Hex:        0x4B     0x4B",
    "Binary:     01001011 01001011",
    "",
    "XOR:        00000011 00000010",
    "Hex:        03       02",
    "",
    "Result: 0302",
  ]),

  h2("Code — ciphers/vernam.py"),
  ...codeBlock(CODE.vernam),
]);

const caesarSection = section("5. Caesar Cipher", [
  h2("How it works"),
  p("The Caesar cipher is the simplest substitution cipher. Each letter in the plaintext is shifted forward in the alphabet by a fixed number (the key), wrapping around from Z back to A. Decryption shifts backward by the same amount."),
  p("The key is a whole number from 1 to 25. Case is preserved and non-letters pass through unchanged. A shift of 13 produces ROT13, which is self-inverse — encrypting twice with key 13 returns the original text."),

  h2("Worked example"),
  p("Key: 3    Plaintext: HELLO"),
  ...exampleBlock([
    "H (7)  + 3 = 10 -> K",
    "E (4)  + 3 =  7 -> H",
    "L (11) + 3 = 14 -> O",
    "L (11) + 3 = 14 -> O",
    "O (14) + 3 = 17 -> R",
    "",
    "Result: KHOOR",
  ]),
  p("Wrap-around example with key 3:"),
  ...exampleBlock([
    "X (23) + 3 = 26 mod 26 = 0 -> A",
    "Y (24) + 3 = 27 mod 26 = 1 -> B",
    "Z (25) + 3 = 28 mod 26 = 2 -> C",
    "",
    "XYZ -> ABC",
  ]),

  h2("Code — ciphers/caesar.py"),
  ...codeBlock(CODE.caesar),
]);

// ── Assemble document ─────────────────────────────────────────────────────
const doc = new Document({
  creator: "ITRI 615 Project",
  title: "Classical Cryptography Tool — Cipher Reference",
  styles: {
    default: { document: { run: { font: ARIAL, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: ARIAL },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: ARIAL },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: ARIAL },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [
      ...titlePage,
      ...intro,
      ...substitutionSection,
      ...vigenereSection,
      ...transpositionSection,
      ...vernamSection,
      ...caesarSection,
    ],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  const out = path.join(__dirname, "Cryptography_Reference.docx");
  fs.writeFileSync(out, buffer);
  console.log("Wrote:", out);
});
