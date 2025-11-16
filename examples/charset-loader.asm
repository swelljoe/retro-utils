// --------------------------------------
// KickAssembler BASIC startup
// Auto-run code at $1000
// --------------------------------------
BasicUpstart2(start)


// --------------------------------------
// Code at $1000
// --------------------------------------
* = $1000

// Zero-page temp
.label z_temp = $fb

start:
    jsr init_charset
    jsr fill_screen
loop:
    jmp loop


// --------------------------------------
// Initialize VIC bank and charset pointer
// --------------------------------------
init_charset:

    // Select VIC bank 0 ($0000-$3fff) via $DD00
    lda $dd00
    and #%11111100
    ora #%00000011      // VIC bank 0
    sta $dd00

    // Screen = $0400  → index 1
    // Charset = $2000 → index 4
    // $D018 = %0001 1000 = $18
    lda #$18
    sta $d018

    rts


// --------------------------------------
// Fill screen with chars 0-255 repeated
// --------------------------------------
fill_screen:
    lda #0
    sta z_temp

    ldy #0
    ldx #0

fill_loop:
    lda z_temp
    sta $0400,y        // character
    lda #$01           // color = white
    sta $d800,y

    inc z_temp
    iny
    bne fill_loop      // loop within this page

    inx
    cpx #4             // 4 * 256 = 1024 cells (40x25 screen)
    bne fill_loop

    rts


// --------------------------------------
// Import your charset binary at $2000
// --------------------------------------
* = $2000
hachicro_charset:
    .import source "hachicro.asm"
