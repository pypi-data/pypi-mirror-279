import {
	Component,
	createEffect,
	createSignal,
	onCleanup,
	JSX,
	splitProps,
	Show,
	onMount,
} from "solid-js";
import "./FileDropZone.styl";
import { readJsonFilesFromDataTransfer } from "../utils/fileUtils";

interface FileDropZoneProps {
	onFileDrop: (files: File[]) => void;
	children: JSX.Element;
	draggingClass?: string;
	overClass?: string;
	overlayClass?: string;
}

export const FileDropZone: Component<FileDropZoneProps> = (
	props: FileDropZoneProps
) => {
	const [handlers, { children }] = splitProps(props, ["onFileDrop"]);

	const [isDraggingOver, setIsDraggingOver] = createSignal(false);
	const [isDragging, setIsDragging] = createSignal(false);

	onMount(() => {
		let timeout: ReturnType<typeof setTimeout>;

		const globalDragEnter = (event: DragEvent) => {
			if (event.dataTransfer?.types?.includes("Files")) {
				setIsDragging(true);
			}
		};

		const globalDragOver = () => {
			clearTimeout(timeout);
			timeout = setTimeout(() => {
				setIsDragging(false);
			}, 500);
		};

		document.addEventListener("dragenter", globalDragEnter);
		document.addEventListener("dragover", globalDragOver);

		onCleanup(() => {
			clearTimeout(timeout);
			document.removeEventListener("dragenter", globalDragEnter);
			document.removeEventListener("dragover", globalDragOver);
		});
	});

	const handleDrop = async (event: DragEvent) => {
		event.preventDefault();
		event.stopPropagation();

		if (!event.dataTransfer) {
			return;
		}

		try {
			const jsonData = await readJsonFilesFromDataTransfer(
				event.dataTransfer
			);
			handlers.onFileDrop(jsonData);
			setIsDraggingOver(false);
			setIsDragging(false);
		} catch (error) {
			console.error("Error reading JSON files:", error);
		}
	};

	const handleDragOver = (event: DragEvent) => {
		event.preventDefault();
		setIsDraggingOver(true);
	};

	const handleDragEnter = (event: DragEvent) => {
		event.preventDefault();
		setIsDraggingOver(true);
	};

	const handleDragLeave = (event: DragEvent) => {
		event.preventDefault();

		setIsDraggingOver(false);
		setIsDragging(false);
	};

	return (
		<div
			class="drop-zone"
			classList={{
				dragging: isDragging(),
				draggingOver: isDraggingOver(),
			}}
		>
			{children}

			<Show when={isDraggingOver() || isDragging()}>
				<div
					class="overlay"
					onDrop={handleDrop}
					onDragOver={handleDragOver}
					onDragEnter={handleDragEnter}
					onDragLeave={handleDragLeave}
				/>
			</Show>
		</div>
	);
};
