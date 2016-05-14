
() main () {
	"set_input" recv-name
	(recv-name) api-recv-bool (recv)
	"get_output" send-name
	(send-name send) api-query-bool ()
	(recv) toggle-button (send)
}

(name) api-recv-bool (out) {
	(out) boolean-channel/name (send-name)
	native {
		"void " name "(bool value) {"
			send-name {
				send-name "(value);"
			}
		"}"
	}
}

(name in) api-query-bool () {
	() native::generate-name (var-name)
	native {
		"static volatile bool " var-name " = false;"
	}

	native {
		"bool " name "() {"
			"return " var-name ";"
		"}"
	}

	native {
		"void " handle-name "(bool value) {"
			var-name " = value;"
		"}"
	}
	(in handle-name) boolean-channel/name ()
}

(button) toggle-button (toggle) {
	(button) on-press (do-toggle)
	(do-toggle) cell-toggle (toggle)
}

(toggle) cell-toggle (out) {
	(rev-input) invert (out)
	(toggle out) latch (rev-input)
}

(boolean) on-press (event) {
	/* 2 core methods */
	(boolean) decompose (_ event)
	(_) ignore-event ()
}

(boolean) on-release (event) {
	/* 2 core methods */
	(boolean) decompose (event _)
	(_) ignore-event ()
}

(in) invert (out) {
	() native::generate-name (proc-name)
	(out) boolean-channel/name (send-name)
	native {
		"void " proc-name "(bool value) {"
			send-name {
				send-name "(value);"
			}
		"}"
	}
	(in proc-name) boolean-channel/name ()
}

(event in) latch (out) {
	() native::generate-name (var-name)
	native {
		"static volatile bool " var-name " = false;"
	}

	() native::generate-name (recv-proc-name)
	native {
		"void " recv-proc-name "(bool value) {"
			var_name " = value;"
		"}"
	}
	(in recv-proc-name) boolean-channel/name ()

	() native::generate-name (dispatch-proc-name)
	(out) boolean-channel/name (send-proc-name)
	native {
		"void " dispatch-proc-name "() {"
			/* cache the value in case it changes as a result of our change */
			"bool local = " var-name ";"
			send-proc-name {
				send-proc-name "(local);"
			}
		"}"
	}
	(event dispatch-proc-name) event-channel/name ()
}

(input) decompose (on-false on-true) {
	() native::generate-name (proc-name)
	(on-false) event-channel/name (proc-false)
	(on-true) event-channel/name (proc-true)
	native {
		"void " proc-name "(bool value) {"
			"if (value) {"
				proc-true {
					proc-true "();"
				}
			"} else {"
				proc-false {
					proc-false "();"
				}
			"}"
		"}"
	}
	(input proc-name) boolean-channel/name ()
}

(input) ignore-event () {
	() native::generate-name (proc-name)
	native { "void " proc-name "() { }" }
	(input proc-name) event-channel/name ()
}

compound event-channel {
	native::text name[];
}

compound boolean-channel {
	native::text name[];
}
