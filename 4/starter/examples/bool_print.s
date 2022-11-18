

	.globl main
	.text
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $144, %rsp
	/*   %1 = const 0 [TAC] */
	movq $0, -8(%rbp)
	/*   jmp %.L2 [TAC] */
	jmp .main.L2
	/*  %.L3: [TAC] */
.main.L3:
	/*   jmp %.L4 [TAC] */
	/* --jmp .main.L4-- */
	/*  %.L4: [TAC] */
.main.L4:
	/*   jmp %.L8 [TAC] */
	/* --jmp .main.L8-- */
	/*  %.L8: [TAC] */
.main.L8:
	/*   jmp %.L7 [TAC] */
	/* --jmp .main.L7-- */
	/*  %.L7: [TAC] */
.main.L7:
	/*   jmp %.L6 [TAC] */
	/* --jmp .main.L6-- */
	/*  %.L6: [TAC] */
.main.L6:
	/*   jmp %.L2 [TAC] */
	jmp .main.L2
	/*  %.L9: [TAC] */
.main.L9:
	/*   jmp %.L2 [TAC] */
	jmp .main.L2
	/*  %.L5: [TAC] */
.main.L5:
	/*   jmp %.L1 [TAC] */
	jmp .main.L1
	/*  %.L2: [TAC] */
.main.L2:
	/*   jmp %.L11 [TAC] */
	jmp .main.L11
	/*  %.L12: [TAC] */
.main.L12:
	/*   jmp %.L11 [TAC] */
	/* --jmp .main.L11-- */
	/*  %.L11: [TAC] */
.main.L11:
	/*   jmp %.L0 [TAC] */
	jmp .main.L0
	/*  %.L10: [TAC] */
.main.L10:
	/*   jmp %.L0 [TAC] */
	/* --jmp .main.L0-- */
	/*  %.L0: [TAC] */
.main.L0:
	/*   %1 = const 1 [TAC] */
	movq $1, -8(%rbp)
	/*  %.L1: [TAC] */
.main.L1:
	/*   %0 = copy %1 [TAC] */
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -16(%rbp), %rdi
	callq __bx_print_bool
	/*   %3 = const 0 [TAC] */
	movq $0, -24(%rbp)
	/*   jmp %.L18 [TAC] */
	/* --jmp .main.L18-- */
	/*  %.L18: [TAC] */
.main.L18:
	/*   jmp %.L16 [TAC] */
	jmp .main.L16
	/*  %.L17: [TAC] */
.main.L17:
	/*   jmp %.L16 [TAC] */
	/* --jmp .main.L16-- */
	/*  %.L16: [TAC] */
.main.L16:
	/*   jmp %.L20 [TAC] */
	/* --jmp .main.L20-- */
	/*  %.L20: [TAC] */
.main.L20:
	/*   jmp %.L21 [TAC] */
	/* --jmp .main.L21-- */
	/*  %.L21: [TAC] */
.main.L21:
	/*   jmp %.L22 [TAC] */
	/* --jmp .main.L22-- */
	/*  %.L22: [TAC] */
.main.L22:
	/*   jmp %.L23 [TAC] */
	/* --jmp .main.L23-- */
	/*  %.L23: [TAC] */
.main.L23:
	/*   jmp %.L19 [TAC] */
	/* --jmp .main.L19-- */
	/*  %.L19: [TAC] */
.main.L19:
	/*   jmp %.L15 [TAC] */
	/* --jmp .main.L15-- */
	/*  %.L15: [TAC] */
.main.L15:
	/*   jmp %.L25 [TAC] */
	/* --jmp .main.L25-- */
	/*  %.L25: [TAC] */
.main.L25:
	/*   jmp %.L24 [TAC] */
	/* --jmp .main.L24-- */
	/*  %.L24: [TAC] */
.main.L24:
	/*   jmp %.L27 [TAC] */
	/* --jmp .main.L27-- */
	/*  %.L27: [TAC] */
.main.L27:
	/*   jmp %.L26 [TAC] */
	jmp .main.L26
	/*  %.L29: [TAC] */
.main.L29:
	/*   jmp %.L26 [TAC] */
	jmp .main.L26
	/*  %.L28: [TAC] */
.main.L28:
	/*   jmp %.L26 [TAC] */
	/* --jmp .main.L26-- */
	/*  %.L26: [TAC] */
.main.L26:
	/*   jmp %.L30 [TAC] */
	/* --jmp .main.L30-- */
	/*  %.L30: [TAC] */
.main.L30:
	/*   jmp %.L13 [TAC] */
	/* --jmp .main.L13-- */
	/*  %.L13: [TAC] */
.main.L13:
	/*   %3 = const 1 [TAC] */
	movq $1, -24(%rbp)
	/*  %.L14: [TAC] */
.main.L14:
	/*   %2 = copy %3 [TAC] */
	movq -24(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -32(%rbp), %rdi
	callq __bx_print_bool
	/*   %5 = const 0 [TAC] */
	movq $0, -40(%rbp)
	/*   jmp %.L38 [TAC] */
	/* --jmp .main.L38-- */
	/*  %.L38: [TAC] */
.main.L38:
	/*   jmp %.L37 [TAC] */
	/* --jmp .main.L37-- */
	/*  %.L37: [TAC] */
.main.L37:
	/*   jmp %.L36 [TAC] */
	/* --jmp .main.L36-- */
	/*  %.L36: [TAC] */
.main.L36:
	/*   jmp %.L34 [TAC] */
	jmp .main.L34
	/*  %.L35: [TAC] */
.main.L35:
	/*   jmp %.L39 [TAC] */
	/* --jmp .main.L39-- */
	/*  %.L39: [TAC] */
.main.L39:
	/*   jmp %.L41 [TAC] */
	/* --jmp .main.L41-- */
	/*  %.L41: [TAC] */
.main.L41:
	/*   jmp %.L42 [TAC] */
	/* --jmp .main.L42-- */
	/*  %.L42: [TAC] */
.main.L42:
	/*   jmp %.L40 [TAC] */
	/* --jmp .main.L40-- */
	/*  %.L40: [TAC] */
.main.L40:
	/*   jmp %.L32 [TAC] */
	jmp .main.L32
	/*  %.L34: [TAC] */
.main.L34:
	/*   jmp %.L44 [TAC] */
	/* --jmp .main.L44-- */
	/*  %.L44: [TAC] */
.main.L44:
	/*   jmp %.L43 [TAC] */
	/* --jmp .main.L43-- */
	/*  %.L43: [TAC] */
.main.L43:
	/*   jmp %.L33 [TAC] */
	jmp .main.L33
	/*  %.L45: [TAC] */
.main.L45:
	/*   jmp %.L33 [TAC] */
	/* --jmp .main.L33-- */
	/*  %.L33: [TAC] */
.main.L33:
	/*   jmp %.L47 [TAC] */
	/* --jmp .main.L47-- */
	/*  %.L47: [TAC] */
.main.L47:
	/*   jmp %.L46 [TAC] */
	/* --jmp .main.L46-- */
	/*  %.L46: [TAC] */
.main.L46:
	/*   jmp %.L50 [TAC] */
	/* --jmp .main.L50-- */
	/*  %.L50: [TAC] */
.main.L50:
	/*   jmp %.L52 [TAC] */
	/* --jmp .main.L52-- */
	/*  %.L52: [TAC] */
.main.L52:
	/*   jmp %.L51 [TAC] */
	jmp .main.L51
	/*  %.L53: [TAC] */
.main.L53:
	/*   jmp %.L57 [TAC] */
	/* --jmp .main.L57-- */
	/*  %.L57: [TAC] */
.main.L57:
	/*   jmp %.L56 [TAC] */
	/* --jmp .main.L56-- */
	/*  %.L56: [TAC] */
.main.L56:
	/*   jmp %.L55 [TAC] */
	/* --jmp .main.L55-- */
	/*  %.L55: [TAC] */
.main.L55:
	/*   jmp %.L49 [TAC] */
	jmp .main.L49
	/*  %.L59: [TAC] */
.main.L59:
	/*   jmp %.L58 [TAC] */
	jmp .main.L58
	/*  %.L61: [TAC] */
.main.L61:
	/*   jmp %.L60 [TAC] */
	/* --jmp .main.L60-- */
	/*  %.L60: [TAC] */
.main.L60:
	/*   jmp %.L58 [TAC] */
	/* --jmp .main.L58-- */
	/*  %.L58: [TAC] */
.main.L58:
	/*   jmp %.L54 [TAC] */
	/* --jmp .main.L54-- */
	/*  %.L54: [TAC] */
.main.L54:
	/*   jmp %.L51 [TAC] */
	/* --jmp .main.L51-- */
	/*  %.L51: [TAC] */
.main.L51:
	/*   jmp %.L48 [TAC] */
	jmp .main.L48
	/*  %.L49: [TAC] */
.main.L49:
	/*   jmp %.L48 [TAC] */
	/* --jmp .main.L48-- */
	/*  %.L48: [TAC] */
.main.L48:
	/*   jmp %.L62 [TAC] */
	/* --jmp .main.L62-- */
	/*  %.L62: [TAC] */
.main.L62:
	/*   jmp %.L63 [TAC] */
	/* --jmp .main.L63-- */
	/*  %.L63: [TAC] */
.main.L63:
	/*   jmp %.L64 [TAC] */
	/* --jmp .main.L64-- */
	/*  %.L64: [TAC] */
.main.L64:
	/*   jmp %.L31 [TAC] */
	/* --jmp .main.L31-- */
	/*  %.L31: [TAC] */
.main.L31:
	/*   %5 = const 1 [TAC] */
	movq $1, -40(%rbp)
	/*  %.L32: [TAC] */
.main.L32:
	/*   %4 = copy %5 [TAC] */
	movq -40(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -48(%rbp), %rdi
	callq __bx_print_bool
	/*   %7 = const 0 [TAC] */
	movq $0, -56(%rbp)
	/*   jmp %.L70 [TAC] */
	/* --jmp .main.L70-- */
	/*  %.L70: [TAC] */
.main.L70:
	/*   jmp %.L69 [TAC] */
	/* --jmp .main.L69-- */
	/*  %.L69: [TAC] */
.main.L69:
	/*   jmp %.L68 [TAC] */
	/* --jmp .main.L68-- */
	/*  %.L68: [TAC] */
.main.L68:
	/*   jmp %.L73 [TAC] */
	/* --jmp .main.L73-- */
	/*  %.L73: [TAC] */
.main.L73:
	/*   jmp %.L72 [TAC] */
	/* --jmp .main.L72-- */
	/*  %.L72: [TAC] */
.main.L72:
	/*   jmp %.L71 [TAC] */
	jmp .main.L71
	/*  %.L74: [TAC] */
.main.L74:
	/*   jmp %.L67 [TAC] */
	jmp .main.L67
	/*  %.L75: [TAC] */
.main.L75:
	/*   jmp %.L71 [TAC] */
	/* --jmp .main.L71-- */
	/*  %.L71: [TAC] */
.main.L71:
	/*   jmp %.L76 [TAC] */
	jmp .main.L76
	/*  %.L77: [TAC] */
.main.L77:
	/*   jmp %.L76 [TAC] */
	jmp .main.L76
	/*  %.L78: [TAC] */
.main.L78:
	/*   jmp %.L79 [TAC] */
	/* --jmp .main.L79-- */
	/*  %.L79: [TAC] */
.main.L79:
	/*   jmp %.L67 [TAC] */
	jmp .main.L67
	/*  %.L76: [TAC] */
.main.L76:
	/*   jmp %.L65 [TAC] */
	jmp .main.L65
	/*  %.L67: [TAC] */
.main.L67:
	/*   jmp %.L82 [TAC] */
	/* --jmp .main.L82-- */
	/*  %.L82: [TAC] */
.main.L82:
	/*   jmp %.L84 [TAC] */
	/* --jmp .main.L84-- */
	/*  %.L84: [TAC] */
.main.L84:
	/*   jmp %.L83 [TAC] */
	jmp .main.L83
	/*  %.L86: [TAC] */
.main.L86:
	/*   jmp %.L85 [TAC] */
	/* --jmp .main.L85-- */
	/*  %.L85: [TAC] */
.main.L85:
	/*   jmp %.L81 [TAC] */
	jmp .main.L81
	/*  %.L83: [TAC] */
.main.L83:
	/*   jmp %.L80 [TAC] */
	jmp .main.L80
	/*  %.L81: [TAC] */
.main.L81:
	/*   jmp %.L87 [TAC] */
	jmp .main.L87
	/*  %.L88: [TAC] */
.main.L88:
	/*   jmp %.L66 [TAC] */
	jmp .main.L66
	/*  %.L87: [TAC] */
.main.L87:
	/*   jmp %.L66 [TAC] */
	jmp .main.L66
	/*  %.L80: [TAC] */
.main.L80:
	/*   jmp %.L92 [TAC] */
	/* --jmp .main.L92-- */
	/*  %.L92: [TAC] */
.main.L92:
	/*   jmp %.L96 [TAC] */
	jmp .main.L96
	/*  %.L97: [TAC] */
.main.L97:
	/*   jmp %.L98 [TAC] */
	jmp .main.L98
	/*  %.L99: [TAC] */
.main.L99:
	/*   jmp %.L100 [TAC] */
	/* --jmp .main.L100-- */
	/*  %.L100: [TAC] */
.main.L100:
	/*   jmp %.L102 [TAC] */
	/* --jmp .main.L102-- */
	/*  %.L102: [TAC] */
.main.L102:
	/*   jmp %.L101 [TAC] */
	jmp .main.L101
	/*  %.L103: [TAC] */
.main.L103:
	/*   jmp %.L95 [TAC] */
	jmp .main.L95
	/*  %.L101: [TAC] */
.main.L101:
	/*   jmp %.L98 [TAC] */
	/* --jmp .main.L98-- */
	/*  %.L98: [TAC] */
.main.L98:
	/*   jmp %.L104 [TAC] */
	/* --jmp .main.L104-- */
	/*  %.L104: [TAC] */
.main.L104:
	/*   jmp %.L96 [TAC] */
	/* --jmp .main.L96-- */
	/*  %.L96: [TAC] */
.main.L96:
	/*   jmp %.L106 [TAC] */
	/* --jmp .main.L106-- */
	/*  %.L106: [TAC] */
.main.L106:
	/*   jmp %.L105 [TAC] */
	/* --jmp .main.L105-- */
	/*  %.L105: [TAC] */
.main.L105:
	/*   jmp %.L95 [TAC] */
	/* --jmp .main.L95-- */
	/*  %.L95: [TAC] */
.main.L95:
	/*   jmp %.L94 [TAC] */
	/* --jmp .main.L94-- */
	/*  %.L94: [TAC] */
.main.L94:
	/*   jmp %.L93 [TAC] */
	/* --jmp .main.L93-- */
	/*  %.L93: [TAC] */
.main.L93:
	/*   jmp %.L108 [TAC] */
	jmp .main.L108
	/*  %.L109: [TAC] */
.main.L109:
	/*   jmp %.L112 [TAC] */
	/* --jmp .main.L112-- */
	/*  %.L112: [TAC] */
.main.L112:
	/*   jmp %.L110 [TAC] */
	jmp .main.L110
	/*  %.L111: [TAC] */
.main.L111:
	/*   jmp %.L110 [TAC] */
	/* --jmp .main.L110-- */
	/*  %.L110: [TAC] */
.main.L110:
	/*   jmp %.L113 [TAC] */
	/* --jmp .main.L113-- */
	/*  %.L113: [TAC] */
.main.L113:
	/*   jmp %.L90 [TAC] */
	jmp .main.L90
	/*  %.L108: [TAC] */
.main.L108:
	/*   jmp %.L107 [TAC] */
	/* --jmp .main.L107-- */
	/*  %.L107: [TAC] */
.main.L107:
	/*   jmp %.L115 [TAC] */
	/* --jmp .main.L115-- */
	/*  %.L115: [TAC] */
.main.L115:
	/*   jmp %.L91 [TAC] */
	jmp .main.L91
	/*  %.L116: [TAC] */
.main.L116:
	/*   jmp %.L114 [TAC] */
	/* --jmp .main.L114-- */
	/*  %.L114: [TAC] */
.main.L114:
	/*   jmp %.L91 [TAC] */
	jmp .main.L91
	/*  %.L117: [TAC] */
.main.L117:
	/*   jmp %.L91 [TAC] */
	/* --jmp .main.L91-- */
	/*  %.L91: [TAC] */
.main.L91:
	/*   jmp %.L89 [TAC] */
	jmp .main.L89
	/*  %.L90: [TAC] */
.main.L90:
	/*   jmp %.L119 [TAC] */
	/* --jmp .main.L119-- */
	/*  %.L119: [TAC] */
.main.L119:
	/*   jmp %.L120 [TAC] */
	/* --jmp .main.L120-- */
	/*  %.L120: [TAC] */
.main.L120:
	/*   jmp %.L122 [TAC] */
	/* --jmp .main.L122-- */
	/*  %.L122: [TAC] */
.main.L122:
	/*   jmp %.L121 [TAC] */
	/* --jmp .main.L121-- */
	/*  %.L121: [TAC] */
.main.L121:
	/*   jmp %.L118 [TAC] */
	/* --jmp .main.L118-- */
	/*  %.L118: [TAC] */
.main.L118:
	/*   jmp %.L66 [TAC] */
	jmp .main.L66
	/*  %.L123: [TAC] */
.main.L123:
	/*   jmp %.L124 [TAC] */
	jmp .main.L124
	/*  %.L126: [TAC] */
.main.L126:
	/*   jmp %.L128 [TAC] */
	/* --jmp .main.L128-- */
	/*  %.L128: [TAC] */
.main.L128:
	/*   jmp %.L129 [TAC] */
	/* --jmp .main.L129-- */
	/*  %.L129: [TAC] */
.main.L129:
	/*   jmp %.L125 [TAC] */
	jmp .main.L125
	/*  %.L127: [TAC] */
.main.L127:
	/*   jmp %.L130 [TAC] */
	/* --jmp .main.L130-- */
	/*  %.L130: [TAC] */
.main.L130:
	/*   jmp %.L131 [TAC] */
	/* --jmp .main.L131-- */
	/*  %.L131: [TAC] */
.main.L131:
	/*   jmp %.L124 [TAC] */
	jmp .main.L124
	/*  %.L125: [TAC] */
.main.L125:
	/*   jmp %.L89 [TAC] */
	jmp .main.L89
	/*  %.L124: [TAC] */
.main.L124:
	/*   jmp %.L132 [TAC] */
	/* --jmp .main.L132-- */
	/*  %.L132: [TAC] */
.main.L132:
	/*   jmp %.L133 [TAC] */
	/* --jmp .main.L133-- */
	/*  %.L133: [TAC] */
.main.L133:
	/*   jmp %.L66 [TAC] */
	jmp .main.L66
	/*  %.L134: [TAC] */
.main.L134:
	/*   jmp %.L66 [TAC] */
	jmp .main.L66
	/*  %.L89: [TAC] */
.main.L89:
	/*   jmp %.L65 [TAC] */
	/* --jmp .main.L65-- */
	/*  %.L65: [TAC] */
.main.L65:
	/*   %7 = const 1 [TAC] */
	movq $1, -56(%rbp)
	/*  %.L66: [TAC] */
.main.L66:
	/*   %6 = copy %7 [TAC] */
	movq -56(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -64(%rbp), %rdi
	callq __bx_print_bool
	/*   %9 = const 0 [TAC] */
	movq $0, -72(%rbp)
	/*   jmp %.L138 [TAC] */
	jmp .main.L138
	/*  %.L140: [TAC] */
.main.L140:
	/*   jmp %.L141 [TAC] */
	/* --jmp .main.L141-- */
	/*  %.L141: [TAC] */
.main.L141:
	/*   jmp %.L139 [TAC] */
	/* --jmp .main.L139-- */
	/*  %.L139: [TAC] */
.main.L139:
	/*   jmp %.L143 [TAC] */
	jmp .main.L143
	/*  %.L144: [TAC] */
.main.L144:
	/*   jmp %.L145 [TAC] */
	/* --jmp .main.L145-- */
	/*  %.L145: [TAC] */
.main.L145:
	/*   jmp %.L146 [TAC] */
	/* --jmp .main.L146-- */
	/*  %.L146: [TAC] */
.main.L146:
	/*   jmp %.L138 [TAC] */
	jmp .main.L138
	/*  %.L143: [TAC] */
.main.L143:
	/*   jmp %.L142 [TAC] */
	/* --jmp .main.L142-- */
	/*  %.L142: [TAC] */
.main.L142:
	/*   jmp %.L137 [TAC] */
	jmp .main.L137
	/*  %.L138: [TAC] */
.main.L138:
	/*   jmp %.L136 [TAC] */
	jmp .main.L136
	/*  %.L137: [TAC] */
.main.L137:
	/*   jmp %.L147 [TAC] */
	/* --jmp .main.L147-- */
	/*  %.L147: [TAC] */
.main.L147:
	/*   jmp %.L149 [TAC] */
	/* --jmp .main.L149-- */
	/*  %.L149: [TAC] */
.main.L149:
	/*   jmp %.L150 [TAC] */
	/* --jmp .main.L150-- */
	/*  %.L150: [TAC] */
.main.L150:
	/*   jmp %.L136 [TAC] */
	jmp .main.L136
	/*  %.L148: [TAC] */
.main.L148:
	/*   jmp %.L136 [TAC] */
	jmp .main.L136
	/*  %.L135: [TAC] */
.main.L135:
	/*   %9 = const 1 [TAC] */
	movq $1, -72(%rbp)
	/*  %.L136: [TAC] */
.main.L136:
	/*   %8 = copy %9 [TAC] */
	movq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	callq __bx_print_bool
	/*   %11 = const 0 [TAC] */
	movq $0, -88(%rbp)
	/*   jmp %.L155 [TAC] */
	/* --jmp .main.L155-- */
	/*  %.L155: [TAC] */
.main.L155:
	/*   jmp %.L154 [TAC] */
	/* --jmp .main.L154-- */
	/*  %.L154: [TAC] */
.main.L154:
	/*   jmp %.L153 [TAC] */
	/* --jmp .main.L153-- */
	/*  %.L153: [TAC] */
.main.L153:
	/*   jmp %.L157 [TAC] */
	/* --jmp .main.L157-- */
	/*  %.L157: [TAC] */
.main.L157:
	/*   jmp %.L159 [TAC] */
	/* --jmp .main.L159-- */
	/*  %.L159: [TAC] */
.main.L159:
	/*   jmp %.L160 [TAC] */
	/* --jmp .main.L160-- */
	/*  %.L160: [TAC] */
.main.L160:
	/*   jmp %.L158 [TAC] */
	/* --jmp .main.L158-- */
	/*  %.L158: [TAC] */
.main.L158:
	/*   jmp %.L152 [TAC] */
	jmp .main.L152
	/*  %.L156: [TAC] */
.main.L156:
	/*   jmp %.L161 [TAC] */
	jmp .main.L161
	/*  %.L162: [TAC] */
.main.L162:
	/*   jmp %.L151 [TAC] */
	jmp .main.L151
	/*  %.L161: [TAC] */
.main.L161:
	/*   jmp %.L164 [TAC] */
	/* --jmp .main.L164-- */
	/*  %.L164: [TAC] */
.main.L164:
	/*   jmp %.L166 [TAC] */
	/* --jmp .main.L166-- */
	/*  %.L166: [TAC] */
.main.L166:
	/*   jmp %.L165 [TAC] */
	/* --jmp .main.L165-- */
	/*  %.L165: [TAC] */
.main.L165:
	/*   jmp %.L163 [TAC] */
	/* --jmp .main.L163-- */
	/*  %.L163: [TAC] */
.main.L163:
	/*   jmp %.L167 [TAC] */
	jmp .main.L167
	/*  %.L168: [TAC] */
.main.L168:
	/*   jmp %.L167 [TAC] */
	/* --jmp .main.L167-- */
	/*  %.L167: [TAC] */
.main.L167:
	/*   jmp %.L151 [TAC] */
	/* --jmp .main.L151-- */
	/*  %.L151: [TAC] */
.main.L151:
	/*   %11 = const 1 [TAC] */
	movq $1, -88(%rbp)
	/*  %.L152: [TAC] */
.main.L152:
	/*   %10 = copy %11 [TAC] */
	movq -88(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -96(%rbp), %rdi
	callq __bx_print_bool
	/*   %13 = const 0 [TAC] */
	movq $0, -104(%rbp)
	/*   jmp %.L173 [TAC] */
	/* --jmp .main.L173-- */
	/*  %.L173: [TAC] */
.main.L173:
	/*   jmp %.L174 [TAC] */
	/* --jmp .main.L174-- */
	/*  %.L174: [TAC] */
.main.L174:
	/*   jmp %.L175 [TAC] */
	/* --jmp .main.L175-- */
	/*  %.L175: [TAC] */
.main.L175:
	/*   jmp %.L172 [TAC] */
	/* --jmp .main.L172-- */
	/*  %.L172: [TAC] */
.main.L172:
	/*   jmp %.L176 [TAC] */
	/* --jmp .main.L176-- */
	/*  %.L176: [TAC] */
.main.L176:
	/*   jmp %.L178 [TAC] */
	/* --jmp .main.L178-- */
	/*  %.L178: [TAC] */
.main.L178:
	/*   jmp %.L181 [TAC] */
	jmp .main.L181
	/*  %.L182: [TAC] */
.main.L182:
	/*   jmp %.L181 [TAC] */
	/* --jmp .main.L181-- */
	/*  %.L181: [TAC] */
.main.L181:
	/*   jmp %.L183 [TAC] */
	/* --jmp .main.L183-- */
	/*  %.L183: [TAC] */
.main.L183:
	/*   jmp %.L177 [TAC] */
	jmp .main.L177
	/*  %.L180: [TAC] */
.main.L180:
	/*   jmp %.L187 [TAC] */
	/* --jmp .main.L187-- */
	/*  %.L187: [TAC] */
.main.L187:
	/*   jmp %.L186 [TAC] */
	jmp .main.L186
	/*  %.L188: [TAC] */
.main.L188:
	/*   jmp %.L189 [TAC] */
	/* --jmp .main.L189-- */
	/*  %.L189: [TAC] */
.main.L189:
	/*   jmp %.L190 [TAC] */
	/* --jmp .main.L190-- */
	/*  %.L190: [TAC] */
.main.L190:
	/*   jmp %.L185 [TAC] */
	jmp .main.L185
	/*  %.L186: [TAC] */
.main.L186:
	/*   jmp %.L185 [TAC] */
	/* --jmp .main.L185-- */
	/*  %.L185: [TAC] */
.main.L185:
	/*   jmp %.L191 [TAC] */
	jmp .main.L191
	/*  %.L193: [TAC] */
.main.L193:
	/*   jmp %.L192 [TAC] */
	/* --jmp .main.L192-- */
	/*  %.L192: [TAC] */
.main.L192:
	/*   jmp %.L194 [TAC] */
	/* --jmp .main.L194-- */
	/*  %.L194: [TAC] */
.main.L194:
	/*   jmp %.L191 [TAC] */
	/* --jmp .main.L191-- */
	/*  %.L191: [TAC] */
.main.L191:
	/*   jmp %.L184 [TAC] */
	jmp .main.L184
	/*  %.L195: [TAC] */
.main.L195:
	/*   jmp %.L184 [TAC] */
	jmp .main.L184
	/*  %.L196: [TAC] */
.main.L196:
	/*   jmp %.L177 [TAC] */
	jmp .main.L177
	/*  %.L184: [TAC] */
.main.L184:
	/*   jmp %.L179 [TAC] */
	/* --jmp .main.L179-- */
	/*  %.L179: [TAC] */
.main.L179:
	/*   jmp %.L170 [TAC] */
	jmp .main.L170
	/*  %.L177: [TAC] */
.main.L177:
	/*   jmp %.L197 [TAC] */
	/* --jmp .main.L197-- */
	/*  %.L197: [TAC] */
.main.L197:
	/*   jmp %.L198 [TAC] */
	/* --jmp .main.L198-- */
	/*  %.L198: [TAC] */
.main.L198:
	/*   jmp %.L171 [TAC] */
	jmp .main.L171
	/*  %.L199: [TAC] */
.main.L199:
	/*   jmp %.L171 [TAC] */
	/* --jmp .main.L171-- */
	/*  %.L171: [TAC] */
.main.L171:
	/*   jmp %.L170 [TAC] */
	jmp .main.L170
	/*  %.L200: [TAC] */
.main.L200:
	/*   jmp %.L170 [TAC] */
	jmp .main.L170
	/*  %.L202: [TAC] */
.main.L202:
	/*   jmp %.L170 [TAC] */
	jmp .main.L170
	/*  %.L201: [TAC] */
.main.L201:
	/*   jmp %.L169 [TAC] */
	/* --jmp .main.L169-- */
	/*  %.L169: [TAC] */
.main.L169:
	/*   %13 = const 1 [TAC] */
	movq $1, -104(%rbp)
	/*  %.L170: [TAC] */
.main.L170:
	/*   %12 = copy %13 [TAC] */
	movq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -112(%rbp), %rdi
	callq __bx_print_bool
	/*   %15 = const 0 [TAC] */
	movq $0, -120(%rbp)
	/*   jmp %.L207 [TAC] */
	jmp .main.L207
	/*  %.L208: [TAC] */
.main.L208:
	/*   jmp %.L206 [TAC] */
	jmp .main.L206
	/*  %.L207: [TAC] */
.main.L207:
	/*   jmp %.L209 [TAC] */
	/* --jmp .main.L209-- */
	/*  %.L209: [TAC] */
.main.L209:
	/*   jmp %.L205 [TAC] */
	jmp .main.L205
	/*  %.L206: [TAC] */
.main.L206:
	/*   jmp %.L212 [TAC] */
	/* --jmp .main.L212-- */
	/*  %.L212: [TAC] */
.main.L212:
	/*   jmp %.L214 [TAC] */
	jmp .main.L214
	/*  %.L217: [TAC] */
.main.L217:
	/*   jmp %.L221 [TAC] */
	/* --jmp .main.L221-- */
	/*  %.L221: [TAC] */
.main.L221:
	/*   jmp %.L220 [TAC] */
	/* --jmp .main.L220-- */
	/*  %.L220: [TAC] */
.main.L220:
	/*   jmp %.L223 [TAC] */
	/* --jmp .main.L223-- */
	/*  %.L223: [TAC] */
.main.L223:
	/*   jmp %.L222 [TAC] */
	/* --jmp .main.L222-- */
	/*  %.L222: [TAC] */
.main.L222:
	/*   jmp %.L219 [TAC] */
	/* --jmp .main.L219-- */
	/*  %.L219: [TAC] */
.main.L219:
	/*   jmp %.L216 [TAC] */
	jmp .main.L216
	/*  %.L218: [TAC] */
.main.L218:
	/*   jmp %.L216 [TAC] */
	/* --jmp .main.L216-- */
	/*  %.L216: [TAC] */
.main.L216:
	/*   jmp %.L224 [TAC] */
	/* --jmp .main.L224-- */
	/*  %.L224: [TAC] */
.main.L224:
	/*   jmp %.L215 [TAC] */
	/* --jmp .main.L215-- */
	/*  %.L215: [TAC] */
.main.L215:
	/*   jmp %.L228 [TAC] */
	/* --jmp .main.L228-- */
	/*  %.L228: [TAC] */
.main.L228:
	/*   jmp %.L230 [TAC] */
	/* --jmp .main.L230-- */
	/*  %.L230: [TAC] */
.main.L230:
	/*   jmp %.L231 [TAC] */
	/* --jmp .main.L231-- */
	/*  %.L231: [TAC] */
.main.L231:
	/*   jmp %.L229 [TAC] */
	/* --jmp .main.L229-- */
	/*  %.L229: [TAC] */
.main.L229:
	/*   jmp %.L232 [TAC] */
	/* --jmp .main.L232-- */
	/*  %.L232: [TAC] */
.main.L232:
	/*   jmp %.L227 [TAC] */
	/* --jmp .main.L227-- */
	/*  %.L227: [TAC] */
.main.L227:
	/*   jmp %.L226 [TAC] */
	/* --jmp .main.L226-- */
	/*  %.L226: [TAC] */
.main.L226:
	/*   jmp %.L234 [TAC] */
	/* --jmp .main.L234-- */
	/*  %.L234: [TAC] */
.main.L234:
	/*   jmp %.L233 [TAC] */
	/* --jmp .main.L233-- */
	/*  %.L233: [TAC] */
.main.L233:
	/*   jmp %.L225 [TAC] */
	/* --jmp .main.L225-- */
	/*  %.L225: [TAC] */
.main.L225:
	/*   jmp %.L236 [TAC] */
	/* --jmp .main.L236-- */
	/*  %.L236: [TAC] */
.main.L236:
	/*   jmp %.L235 [TAC] */
	/* --jmp .main.L235-- */
	/*  %.L235: [TAC] */
.main.L235:
	/*   jmp %.L238 [TAC] */
	/* --jmp .main.L238-- */
	/*  %.L238: [TAC] */
.main.L238:
	/*   jmp %.L237 [TAC] */
	/* --jmp .main.L237-- */
	/*  %.L237: [TAC] */
.main.L237:
	/*   jmp %.L210 [TAC] */
	jmp .main.L210
	/*  %.L214: [TAC] */
.main.L214:
	/*   jmp %.L210 [TAC] */
	jmp .main.L210
	/*  %.L213: [TAC] */
.main.L213:
	/*   jmp %.L210 [TAC] */
	jmp .main.L210
	/*  %.L211: [TAC] */
.main.L211:
	/*   jmp %.L244 [TAC] */
	/* --jmp .main.L244-- */
	/*  %.L244: [TAC] */
.main.L244:
	/*   jmp %.L245 [TAC] */
	/* --jmp .main.L245-- */
	/*  %.L245: [TAC] */
.main.L245:
	/*   jmp %.L243 [TAC] */
	/* --jmp .main.L243-- */
	/*  %.L243: [TAC] */
.main.L243:
	/*   jmp %.L246 [TAC] */
	/* --jmp .main.L246-- */
	/*  %.L246: [TAC] */
.main.L246:
	/*   jmp %.L241 [TAC] */
	jmp .main.L241
	/*  %.L242: [TAC] */
.main.L242:
	/*   jmp %.L249 [TAC] */
	/* --jmp .main.L249-- */
	/*  %.L249: [TAC] */
.main.L249:
	/*   jmp %.L250 [TAC] */
	/* --jmp .main.L250-- */
	/*  %.L250: [TAC] */
.main.L250:
	/*   jmp %.L248 [TAC] */
	/* --jmp .main.L248-- */
	/*  %.L248: [TAC] */
.main.L248:
	/*   jmp %.L254 [TAC] */
	/* --jmp .main.L254-- */
	/*  %.L254: [TAC] */
.main.L254:
	/*   jmp %.L253 [TAC] */
	/* --jmp .main.L253-- */
	/*  %.L253: [TAC] */
.main.L253:
	/*   jmp %.L255 [TAC] */
	jmp .main.L255
	/*  %.L256: [TAC] */
.main.L256:
	/*   jmp %.L241 [TAC] */
	jmp .main.L241
	/*  %.L255: [TAC] */
.main.L255:
	/*   jmp %.L252 [TAC] */
	/* --jmp .main.L252-- */
	/*  %.L252: [TAC] */
.main.L252:
	/*   jmp %.L251 [TAC] */
	/* --jmp .main.L251-- */
	/*  %.L251: [TAC] */
.main.L251:
	/*   jmp %.L257 [TAC] */
	/* --jmp .main.L257-- */
	/*  %.L257: [TAC] */
.main.L257:
	/*   jmp %.L258 [TAC] */
	/* --jmp .main.L258-- */
	/*  %.L258: [TAC] */
.main.L258:
	/*   jmp %.L247 [TAC] */
	/* --jmp .main.L247-- */
	/*  %.L247: [TAC] */
.main.L247:
	/*   jmp %.L259 [TAC] */
	/* --jmp .main.L259-- */
	/*  %.L259: [TAC] */
.main.L259:
	/*   jmp %.L260 [TAC] */
	/* --jmp .main.L260-- */
	/*  %.L260: [TAC] */
.main.L260:
	/*   jmp %.L239 [TAC] */
	jmp .main.L239
	/*  %.L241: [TAC] */
.main.L241:
	/*   jmp %.L239 [TAC] */
	jmp .main.L239
	/*  %.L240: [TAC] */
.main.L240:
	/*   jmp %.L210 [TAC] */
	jmp .main.L210
	/*  %.L239: [TAC] */
.main.L239:
	/*   jmp %.L203 [TAC] */
	jmp .main.L203
	/*  %.L210: [TAC] */
.main.L210:
	/*   jmp %.L261 [TAC] */
	jmp .main.L261
	/*  %.L262: [TAC] */
.main.L262:
	/*   jmp %.L261 [TAC] */
	/* --jmp .main.L261-- */
	/*  %.L261: [TAC] */
.main.L261:
	/*   jmp %.L203 [TAC] */
	jmp .main.L203
	/*  %.L205: [TAC] */
.main.L205:
	/*   jmp %.L264 [TAC] */
	jmp .main.L264
	/*  %.L265: [TAC] */
.main.L265:
	/*   jmp %.L266 [TAC] */
	/* --jmp .main.L266-- */
	/*  %.L266: [TAC] */
.main.L266:
	/*   jmp %.L267 [TAC] */
	/* --jmp .main.L267-- */
	/*  %.L267: [TAC] */
.main.L267:
	/*   jmp %.L263 [TAC] */
	jmp .main.L263
	/*  %.L264: [TAC] */
.main.L264:
	/*   jmp %.L268 [TAC] */
	jmp .main.L268
	/*  %.L269: [TAC] */
.main.L269:
	/*   jmp %.L268 [TAC] */
	/* --jmp .main.L268-- */
	/*  %.L268: [TAC] */
.main.L268:
	/*   jmp %.L270 [TAC] */
	/* --jmp .main.L270-- */
	/*  %.L270: [TAC] */
.main.L270:
	/*   jmp %.L204 [TAC] */
	jmp .main.L204
	/*  %.L263: [TAC] */
.main.L263:
	/*   jmp %.L204 [TAC] */
	jmp .main.L204
	/*  %.L271: [TAC] */
.main.L271:
	/*   jmp %.L273 [TAC] */
	/* --jmp .main.L273-- */
	/*  %.L273: [TAC] */
.main.L273:
	/*   jmp %.L272 [TAC] */
	/* --jmp .main.L272-- */
	/*  %.L272: [TAC] */
.main.L272:
	/*   jmp %.L204 [TAC] */
	jmp .main.L204
	/*  %.L203: [TAC] */
.main.L203:
	/*   %15 = const 1 [TAC] */
	movq $1, -120(%rbp)
	/*  %.L204: [TAC] */
.main.L204:
	/*   %14 = copy %15 [TAC] */
	movq -120(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -128(%rbp), %rdi
	callq __bx_print_bool
	/*   %17 = const 0 [TAC] */
	movq $0, -136(%rbp)
	/*   jmp %.L282 [TAC] */
	/* --jmp .main.L282-- */
	/*  %.L282: [TAC] */
.main.L282:
	/*   jmp %.L280 [TAC] */
	jmp .main.L280
	/*  %.L283: [TAC] */
.main.L283:
	/*   jmp %.L281 [TAC] */
	/* --jmp .main.L281-- */
	/*  %.L281: [TAC] */
.main.L281:
	/*   jmp %.L278 [TAC] */
	jmp .main.L278
	/*  %.L280: [TAC] */
.main.L280:
	/*   jmp %.L279 [TAC] */
	jmp .main.L279
	/*  %.L284: [TAC] */
.main.L284:
	/*   jmp %.L279 [TAC] */
	/* --jmp .main.L279-- */
	/*  %.L279: [TAC] */
.main.L279:
	/*   jmp %.L277 [TAC] */
	jmp .main.L277
	/*  %.L278: [TAC] */
.main.L278:
	/*   jmp %.L286 [TAC] */
	/* --jmp .main.L286-- */
	/*  %.L286: [TAC] */
.main.L286:
	/*   jmp %.L285 [TAC] */
	/* --jmp .main.L285-- */
	/*  %.L285: [TAC] */
.main.L285:
	/*   jmp %.L275 [TAC] */
	jmp .main.L275
	/*  %.L288: [TAC] */
.main.L288:
	/*   jmp %.L287 [TAC] */
	/* --jmp .main.L287-- */
	/*  %.L287: [TAC] */
.main.L287:
	/*   jmp %.L290 [TAC] */
	/* --jmp .main.L290-- */
	/*  %.L290: [TAC] */
.main.L290:
	/*   jmp %.L277 [TAC] */
	jmp .main.L277
	/*  %.L289: [TAC] */
.main.L289:
	/*   jmp %.L292 [TAC] */
	/* --jmp .main.L292-- */
	/*  %.L292: [TAC] */
.main.L292:
	/*   jmp %.L277 [TAC] */
	jmp .main.L277
	/*  %.L291: [TAC] */
.main.L291:
	/*   jmp %.L277 [TAC] */
	/* --jmp .main.L277-- */
	/*  %.L277: [TAC] */
.main.L277:
	/*   jmp %.L297 [TAC] */
	/* --jmp .main.L297-- */
	/*  %.L297: [TAC] */
.main.L297:
	/*   jmp %.L296 [TAC] */
	/* --jmp .main.L296-- */
	/*  %.L296: [TAC] */
.main.L296:
	/*   jmp %.L293 [TAC] */
	jmp .main.L293
	/*  %.L295: [TAC] */
.main.L295:
	/*   jmp %.L300 [TAC] */
	jmp .main.L300
	/*  %.L301: [TAC] */
.main.L301:
	/*   jmp %.L300 [TAC] */
	/* --jmp .main.L300-- */
	/*  %.L300: [TAC] */
.main.L300:
	/*   jmp %.L302 [TAC] */
	/* --jmp .main.L302-- */
	/*  %.L302: [TAC] */
.main.L302:
	/*   jmp %.L299 [TAC] */
	/* --jmp .main.L299-- */
	/*  %.L299: [TAC] */
.main.L299:
	/*   jmp %.L298 [TAC] */
	/* --jmp .main.L298-- */
	/*  %.L298: [TAC] */
.main.L298:
	/*   jmp %.L294 [TAC] */
	/* --jmp .main.L294-- */
	/*  %.L294: [TAC] */
.main.L294:
	/*   jmp %.L276 [TAC] */
	jmp .main.L276
	/*  %.L304: [TAC] */
.main.L304:
	/*   jmp %.L305 [TAC] */
	/* --jmp .main.L305-- */
	/*  %.L305: [TAC] */
.main.L305:
	/*   jmp %.L276 [TAC] */
	jmp .main.L276
	/*  %.L303: [TAC] */
.main.L303:
	/*   jmp %.L308 [TAC] */
	/* --jmp .main.L308-- */
	/*  %.L308: [TAC] */
.main.L308:
	/*   jmp %.L307 [TAC] */
	/* --jmp .main.L307-- */
	/*  %.L307: [TAC] */
.main.L307:
	/*   jmp %.L309 [TAC] */
	/* --jmp .main.L309-- */
	/*  %.L309: [TAC] */
.main.L309:
	/*   jmp %.L306 [TAC] */
	/* --jmp .main.L306-- */
	/*  %.L306: [TAC] */
.main.L306:
	/*   jmp %.L276 [TAC] */
	jmp .main.L276
	/*  %.L293: [TAC] */
.main.L293:
	/*   jmp %.L311 [TAC] */
	/* --jmp .main.L311-- */
	/*  %.L311: [TAC] */
.main.L311:
	/*   jmp %.L312 [TAC] */
	/* --jmp .main.L312-- */
	/*  %.L312: [TAC] */
.main.L312:
	/*   jmp %.L313 [TAC] */
	/* --jmp .main.L313-- */
	/*  %.L313: [TAC] */
.main.L313:
	/*   jmp %.L315 [TAC] */
	jmp .main.L315
	/*  %.L316: [TAC] */
.main.L316:
	/*   jmp %.L275 [TAC] */
	jmp .main.L275
	/*  %.L315: [TAC] */
.main.L315:
	/*   jmp %.L314 [TAC] */
	/* --jmp .main.L314-- */
	/*  %.L314: [TAC] */
.main.L314:
	/*   jmp %.L310 [TAC] */
	/* --jmp .main.L310-- */
	/*  %.L310: [TAC] */
.main.L310:
	/*   jmp %.L317 [TAC] */
	jmp .main.L317
	/*  %.L318: [TAC] */
.main.L318:
	/*   jmp %.L320 [TAC] */
	/* --jmp .main.L320-- */
	/*  %.L320: [TAC] */
.main.L320:
	/*   jmp %.L319 [TAC] */
	/* --jmp .main.L319-- */
	/*  %.L319: [TAC] */
.main.L319:
	/*   jmp %.L317 [TAC] */
	/* --jmp .main.L317-- */
	/*  %.L317: [TAC] */
.main.L317:
	/*   jmp %.L276 [TAC] */
	/* --jmp .main.L276-- */
	/*  %.L276: [TAC] */
.main.L276:
	/*   jmp %.L321 [TAC] */
	jmp .main.L321
	/*  %.L324: [TAC] */
.main.L324:
	/*   jmp %.L321 [TAC] */
	jmp .main.L321
	/*  %.L323: [TAC] */
.main.L323:
	/*   jmp %.L326 [TAC] */
	/* --jmp .main.L326-- */
	/*  %.L326: [TAC] */
.main.L326:
	/*   jmp %.L325 [TAC] */
	jmp .main.L325
	/*  %.L327: [TAC] */
.main.L327:
	/*   jmp %.L328 [TAC] */
	/* --jmp .main.L328-- */
	/*  %.L328: [TAC] */
.main.L328:
	/*   jmp %.L321 [TAC] */
	jmp .main.L321
	/*  %.L325: [TAC] */
.main.L325:
	/*   jmp %.L321 [TAC] */
	jmp .main.L321
	/*  %.L322: [TAC] */
.main.L322:
	/*   jmp %.L331 [TAC] */
	jmp .main.L331
	/*  %.L332: [TAC] */
.main.L332:
	/*   jmp %.L331 [TAC] */
	/* --jmp .main.L331-- */
	/*  %.L331: [TAC] */
.main.L331:
	/*   jmp %.L329 [TAC] */
	jmp .main.L329
	/*  %.L330: [TAC] */
.main.L330:
	/*   jmp %.L334 [TAC] */
	/* --jmp .main.L334-- */
	/*  %.L334: [TAC] */
.main.L334:
	/*   jmp %.L333 [TAC] */
	/* --jmp .main.L333-- */
	/*  %.L333: [TAC] */
.main.L333:
	/*   jmp %.L336 [TAC] */
	/* --jmp .main.L336-- */
	/*  %.L336: [TAC] */
.main.L336:
	/*   jmp %.L335 [TAC] */
	jmp .main.L335
	/*  %.L337: [TAC] */
.main.L337:
	/*   jmp %.L339 [TAC] */
	/* --jmp .main.L339-- */
	/*  %.L339: [TAC] */
.main.L339:
	/*   jmp %.L338 [TAC] */
	jmp .main.L338
	/*  %.L340: [TAC] */
.main.L340:
	/*   jmp %.L338 [TAC] */
	/* --jmp .main.L338-- */
	/*  %.L338: [TAC] */
.main.L338:
	/*   jmp %.L341 [TAC] */
	/* --jmp .main.L341-- */
	/*  %.L341: [TAC] */
.main.L341:
	/*   jmp %.L335 [TAC] */
	/* --jmp .main.L335-- */
	/*  %.L335: [TAC] */
.main.L335:
	/*   jmp %.L329 [TAC] */
	/* --jmp .main.L329-- */
	/*  %.L329: [TAC] */
.main.L329:
	/*   jmp %.L343 [TAC] */
	/* --jmp .main.L343-- */
	/*  %.L343: [TAC] */
.main.L343:
	/*   jmp %.L344 [TAC] */
	/* --jmp .main.L344-- */
	/*  %.L344: [TAC] */
.main.L344:
	/*   jmp %.L342 [TAC] */
	/* --jmp .main.L342-- */
	/*  %.L342: [TAC] */
.main.L342:
	/*   jmp %.L274 [TAC] */
	jmp .main.L274
	/*  %.L321: [TAC] */
.main.L321:
	/*   jmp %.L349 [TAC] */
	/* --jmp .main.L349-- */
	/*  %.L349: [TAC] */
.main.L349:
	/*   jmp %.L348 [TAC] */
	/* --jmp .main.L348-- */
	/*  %.L348: [TAC] */
.main.L348:
	/*   jmp %.L350 [TAC] */
	/* --jmp .main.L350-- */
	/*  %.L350: [TAC] */
.main.L350:
	/*   jmp %.L351 [TAC] */
	jmp .main.L351
	/*  %.L352: [TAC] */
.main.L352:
	/*   jmp %.L351 [TAC] */
	/* --jmp .main.L351-- */
	/*  %.L351: [TAC] */
.main.L351:
	/*   jmp %.L353 [TAC] */
	/* --jmp .main.L353-- */
	/*  %.L353: [TAC] */
.main.L353:
	/*   jmp %.L355 [TAC] */
	/* --jmp .main.L355-- */
	/*  %.L355: [TAC] */
.main.L355:
	/*   jmp %.L354 [TAC] */
	/* --jmp .main.L354-- */
	/*  %.L354: [TAC] */
.main.L354:
	/*   jmp %.L345 [TAC] */
	jmp .main.L345
	/*  %.L347: [TAC] */
.main.L347:
	/*   jmp %.L359 [TAC] */
	jmp .main.L359
	/*  %.L360: [TAC] */
.main.L360:
	/*   jmp %.L361 [TAC] */
	/* --jmp .main.L361-- */
	/*  %.L361: [TAC] */
.main.L361:
	/*   jmp %.L366 [TAC] */
	/* --jmp .main.L366-- */
	/*  %.L366: [TAC] */
.main.L366:
	/*   jmp %.L372 [TAC] */
	/* --jmp .main.L372-- */
	/*  %.L372: [TAC] */
.main.L372:
	/*   jmp %.L371 [TAC] */
	/* --jmp .main.L371-- */
	/*  %.L371: [TAC] */
.main.L371:
	/*   jmp %.L369 [TAC] */
	jmp .main.L369
	/*  %.L370: [TAC] */
.main.L370:
	/*   jmp %.L364 [TAC] */
	jmp .main.L364
	/*  %.L369: [TAC] */
.main.L369:
	/*   jmp %.L364 [TAC] */
	jmp .main.L364
	/*  %.L368: [TAC] */
.main.L368:
	/*   jmp %.L367 [TAC] */
	jmp .main.L367
	/*  %.L373: [TAC] */
.main.L373:
	/*   jmp %.L367 [TAC] */
	/* --jmp .main.L367-- */
	/*  %.L367: [TAC] */
.main.L367:
	/*   jmp %.L374 [TAC] */
	/* --jmp .main.L374-- */
	/*  %.L374: [TAC] */
.main.L374:
	/*   jmp %.L365 [TAC] */
	jmp .main.L365
	/*  %.L375: [TAC] */
.main.L375:
	/*   jmp %.L376 [TAC] */
	/* --jmp .main.L376-- */
	/*  %.L376: [TAC] */
.main.L376:
	/*   jmp %.L365 [TAC] */
	/* --jmp .main.L365-- */
	/*  %.L365: [TAC] */
.main.L365:
	/*   jmp %.L377 [TAC] */
	/* --jmp .main.L377-- */
	/*  %.L377: [TAC] */
.main.L377:
	/*   jmp %.L380 [TAC] */
	/* --jmp .main.L380-- */
	/*  %.L380: [TAC] */
.main.L380:
	/*   jmp %.L379 [TAC] */
	jmp .main.L379
	/*  %.L381: [TAC] */
.main.L381:
	/*   jmp %.L379 [TAC] */
	/* --jmp .main.L379-- */
	/*  %.L379: [TAC] */
.main.L379:
	/*   jmp %.L378 [TAC] */
	/* --jmp .main.L378-- */
	/*  %.L378: [TAC] */
.main.L378:
	/*   jmp %.L363 [TAC] */
	jmp .main.L363
	/*  %.L364: [TAC] */
.main.L364:
	/*   jmp %.L358 [TAC] */
	jmp .main.L358
	/*  %.L363: [TAC] */
.main.L363:
	/*   jmp %.L362 [TAC] */
	/* --jmp .main.L362-- */
	/*  %.L362: [TAC] */
.main.L362:
	/*   jmp %.L382 [TAC] */
	/* --jmp .main.L382-- */
	/*  %.L382: [TAC] */
.main.L382:
	/*   jmp %.L359 [TAC] */
	/* --jmp .main.L359-- */
	/*  %.L359: [TAC] */
.main.L359:
	/*   jmp %.L357 [TAC] */
	jmp .main.L357
	/*  %.L358: [TAC] */
.main.L358:
	/*   jmp %.L357 [TAC] */
	/* --jmp .main.L357-- */
	/*  %.L357: [TAC] */
.main.L357:
	/*   jmp %.L345 [TAC] */
	jmp .main.L345
	/*  %.L383: [TAC] */
.main.L383:
	/*   jmp %.L345 [TAC] */
	jmp .main.L345
	/*  %.L356: [TAC] */
.main.L356:
	/*   jmp %.L384 [TAC] */
	/* --jmp .main.L384-- */
	/*  %.L384: [TAC] */
.main.L384:
	/*   jmp %.L385 [TAC] */
	/* --jmp .main.L385-- */
	/*  %.L385: [TAC] */
.main.L385:
	/*   jmp %.L346 [TAC] */
	/* --jmp .main.L346-- */
	/*  %.L346: [TAC] */
.main.L346:
	/*   jmp %.L386 [TAC] */
	/* --jmp .main.L386-- */
	/*  %.L386: [TAC] */
.main.L386:
	/*   jmp %.L387 [TAC] */
	jmp .main.L387
	/*  %.L389: [TAC] */
.main.L389:
	/*   jmp %.L387 [TAC] */
	jmp .main.L387
	/*  %.L388: [TAC] */
.main.L388:
	/*   jmp %.L274 [TAC] */
	jmp .main.L274
	/*  %.L390: [TAC] */
.main.L390:
	/*   jmp %.L392 [TAC] */
	/* --jmp .main.L392-- */
	/*  %.L392: [TAC] */
.main.L392:
	/*   jmp %.L391 [TAC] */
	/* --jmp .main.L391-- */
	/*  %.L391: [TAC] */
.main.L391:
	/*   jmp %.L387 [TAC] */
	/* --jmp .main.L387-- */
	/*  %.L387: [TAC] */
.main.L387:
	/*   jmp %.L395 [TAC] */
	/* --jmp .main.L395-- */
	/*  %.L395: [TAC] */
.main.L395:
	/*   jmp %.L396 [TAC] */
	/* --jmp .main.L396-- */
	/*  %.L396: [TAC] */
.main.L396:
	/*   jmp %.L394 [TAC] */
	/* --jmp .main.L394-- */
	/*  %.L394: [TAC] */
.main.L394:
	/*   jmp %.L393 [TAC] */
	/* --jmp .main.L393-- */
	/*  %.L393: [TAC] */
.main.L393:
	/*   jmp %.L397 [TAC] */
	jmp .main.L397
	/*  %.L398: [TAC] */
.main.L398:
	/*   jmp %.L400 [TAC] */
	/* --jmp .main.L400-- */
	/*  %.L400: [TAC] */
.main.L400:
	/*   jmp %.L401 [TAC] */
	jmp .main.L401
	/*  %.L402: [TAC] */
.main.L402:
	/*   jmp %.L404 [TAC] */
	/* --jmp .main.L404-- */
	/*  %.L404: [TAC] */
.main.L404:
	/*   jmp %.L403 [TAC] */
	jmp .main.L403
	/*  %.L405: [TAC] */
.main.L405:
	/*   jmp %.L397 [TAC] */
	jmp .main.L397
	/*  %.L403: [TAC] */
.main.L403:
	/*   jmp %.L401 [TAC] */
	/* --jmp .main.L401-- */
	/*  %.L401: [TAC] */
.main.L401:
	/*   jmp %.L407 [TAC] */
	/* --jmp .main.L407-- */
	/*  %.L407: [TAC] */
.main.L407:
	/*   jmp %.L408 [TAC] */
	/* --jmp .main.L408-- */
	/*  %.L408: [TAC] */
.main.L408:
	/*   jmp %.L409 [TAC] */
	/* --jmp .main.L409-- */
	/*  %.L409: [TAC] */
.main.L409:
	/*   jmp %.L406 [TAC] */
	/* --jmp .main.L406-- */
	/*  %.L406: [TAC] */
.main.L406:
	/*   jmp %.L399 [TAC] */
	/* --jmp .main.L399-- */
	/*  %.L399: [TAC] */
.main.L399:
	/*   jmp %.L274 [TAC] */
	jmp .main.L274
	/*  %.L397: [TAC] */
.main.L397:
	/*   jmp %.L345 [TAC] */
	/* --jmp .main.L345-- */
	/*  %.L345: [TAC] */
.main.L345:
	/*   jmp %.L413 [TAC] */
	/* --jmp .main.L413-- */
	/*  %.L413: [TAC] */
.main.L413:
	/*   jmp %.L415 [TAC] */
	/* --jmp .main.L415-- */
	/*  %.L415: [TAC] */
.main.L415:
	/*   jmp %.L416 [TAC] */
	/* --jmp .main.L416-- */
	/*  %.L416: [TAC] */
.main.L416:
	/*   jmp %.L414 [TAC] */
	/* --jmp .main.L414-- */
	/*  %.L414: [TAC] */
.main.L414:
	/*   jmp %.L412 [TAC] */
	/* --jmp .main.L412-- */
	/*  %.L412: [TAC] */
.main.L412:
	/*   jmp %.L418 [TAC] */
	/* --jmp .main.L418-- */
	/*  %.L418: [TAC] */
.main.L418:
	/*   jmp %.L411 [TAC] */
	jmp .main.L411
	/*  %.L417: [TAC] */
.main.L417:
	/*   jmp %.L274 [TAC] */
	jmp .main.L274
	/*  %.L411: [TAC] */
.main.L411:
	/*   jmp %.L420 [TAC] */
	/* --jmp .main.L420-- */
	/*  %.L420: [TAC] */
.main.L420:
	/*   jmp %.L421 [TAC] */
	/* --jmp .main.L421-- */
	/*  %.L421: [TAC] */
.main.L421:
	/*   jmp %.L410 [TAC] */
	jmp .main.L410
	/*  %.L419: [TAC] */
.main.L419:
	/*   jmp %.L274 [TAC] */
	jmp .main.L274
	/*  %.L410: [TAC] */
.main.L410:
	/*   jmp %.L422 [TAC] */
	jmp .main.L422
	/*  %.L423: [TAC] */
.main.L423:
	/*   jmp %.L424 [TAC] */
	/* --jmp .main.L424-- */
	/*  %.L424: [TAC] */
.main.L424:
	/*   jmp %.L425 [TAC] */
	/* --jmp .main.L425-- */
	/*  %.L425: [TAC] */
.main.L425:
	/*   jmp %.L426 [TAC] */
	/* --jmp .main.L426-- */
	/*  %.L426: [TAC] */
.main.L426:
	/*   jmp %.L422 [TAC] */
	/* --jmp .main.L422-- */
	/*  %.L422: [TAC] */
.main.L422:
	/*   jmp %.L275 [TAC] */
	jmp .main.L275
	/*  %.L428: [TAC] */
.main.L428:
	/*   jmp %.L429 [TAC] */
	/* --jmp .main.L429-- */
	/*  %.L429: [TAC] */
.main.L429:
	/*   jmp %.L430 [TAC] */
	/* --jmp .main.L430-- */
	/*  %.L430: [TAC] */
.main.L430:
	/*   jmp %.L431 [TAC] */
	/* --jmp .main.L431-- */
	/*  %.L431: [TAC] */
.main.L431:
	/*   jmp %.L275 [TAC] */
	jmp .main.L275
	/*  %.L427: [TAC] */
.main.L427:
	/*   jmp %.L274 [TAC] */
	/* --jmp .main.L274-- */
	/*  %.L274: [TAC] */
.main.L274:
	/*   %17 = const 1 [TAC] */
	movq $1, -136(%rbp)
	/*  %.L275: [TAC] */
.main.L275:
	/*   %16 = copy %17 [TAC] */
	movq -136(%rbp), %r11
	movq %r11, -144(%rbp)
	movq -144(%rbp), %rdi
	callq __bx_print_bool
	xorq %rax, %rax
	jmp .main.Lexit
.main.Lexit:
	movq %rbp, %rsp
	popq %rbp
	retq
