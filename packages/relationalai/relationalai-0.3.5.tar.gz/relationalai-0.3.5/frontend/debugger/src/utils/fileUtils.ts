function reviver(key: string|number, value: any) {
	if(key === "time" && typeof value === "string") return new Date(value);
	if(key === "start_time" && typeof value === "string") return new Date(value);
	if(key === "end_time" && typeof value === "string") return new Date(value);
	return value;
}

export async function readJsonFilesFromDataTransfer(
	dataTransfer: DataTransfer
): Promise<any[]> {
	// Extract the list of files from the DataTransfer object
	const files = Array.from(dataTransfer.files);

	// Filter for JSON files only, since we export JSON files
	const jsonFiles = files.filter((file) => file.name.endsWith(".json"));

	if (jsonFiles.length === 0) {
		throw new Error("No JSON files found in the drop zone");
	}

	// Read and parse each JSON file
	const readAndParseFile = (file: File): Promise<any> => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = () => {
				try {
					// Attempt to parse the JSON content
					const result = JSON.parse(reader.result as string, reviver);
					resolve(result);
				} catch (error) {
					reject(error);
				}
			};
			reader.onerror = () => {
				reject(reader.error);
			};
			reader.readAsText(file);
		});
	};

	// Map each JSON file to a promise that resolves to its parsed content
	const promises = jsonFiles.map(readAndParseFile);

	// Wait for all files to be read and parsed
	return Promise.all(promises);
}
