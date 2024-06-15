import { Component } from "solid-js";
import { Message } from "../debugger_client";
import "./Alert.styl";

export const Alert: Component<Message.Warn | Message.Error> = (props) => {
	const isError = (props: Message.Warn | Message.Error): props is Message.Error => {
		return props.event === "error";
	};

	const alertType = isError(props) ? "error" : "warn";
	const alertHeader = props.name || (isError(props) ? props.message || "Error" : "Warning");
	const content = props.raw_content || (isError(props) ? props.err : "");

	return (
		<div class="container">
			<div class="header">
				<span> {alertHeader} </span>

				<span>
					{props.source && props.source.file ? ` ${props.source.file}` : ""}
					{props.source && props.source.line ? `: ${props.source.line}` : ""}
				</span>
			</div>
			<pre class="details">{content}</pre>
		</div>
	);
};
