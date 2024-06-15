import { readJsonFilesFromDataTransfer } from "./fileUtils";

// Helper function to create a mock file
function createMockFile(name: string, type: string): File {
	return new File(["{}"], name, { type });
}

// Helper function to create a DataTransfer mock
function createDataTransferMock(files: File[]): DataTransfer {
	const dataTransfer: Partial<DataTransfer> = {
		files: {
			length: files.length,
			item: (index: number) => files[index],
			[Symbol.iterator]: function* () {
				for (let i = 0; i < files.length; i++) {
					yield files[i];
				}
			} as any,
		},
	};
	return dataTransfer as DataTransfer;
}

const jsonContent: string = JSON.stringify({ key: "value" });

class FileReaderMock {
	static EMPTY = 0;
	static LOADING = 1;
	static DONE = 2;
	readyState = FileReaderMock.EMPTY;
	result: string | null = jsonContent;
	error: DOMException | null = null;

	onload: () => void = () => Promise.resolve(this.result);
	onerror: () => void = () => null;

	readAsText(file: File) {
		// Simulate async file reading
		setTimeout(() => {
			if (file) {
				this.onload();
			} else {
				this.onerror();
			}
		}, 0);
	}
}

const originalFileReader = global.FileReader;

describe("readJsonFilesFromDataTransfer", () => {
	beforeEach(() => {
		global.FileReader = FileReaderMock as any;
	});

	afterEach(() => {
		global.FileReader = originalFileReader;
	});


	it("should throw an error if no JSON files are dropped", async () => {
		const mockFiles: File[] = [
			createMockFile("test.txt", "text/plain"),
		];
		const dataTransfer: DataTransfer = createDataTransferMock(mockFiles);

		await expect(
			readJsonFilesFromDataTransfer(dataTransfer)
		).rejects.toThrow("No JSON files found in the drop zone");
	});

	it("should correctly read and parse JSON files", async () => {
		const mockFiles: File[] = [
			createMockFile("test.json", "application/json"),
		];

		const dataTransfer: DataTransfer = createDataTransferMock(mockFiles);
		const promise = readJsonFilesFromDataTransfer(dataTransfer);

		const result = await promise;

		expect(result).toEqual([{ key: "value" }]);
	});

	it("should handle mixed file types and only parse JSON files", async () => {
		const mockFiles: File[] = [
			createMockFile("test.json", "application/json"),
			createMockFile("image.png", "image/png"),
		];

		const dataTransfer: DataTransfer = createDataTransferMock(mockFiles);
		const result: any[] = await readJsonFilesFromDataTransfer(dataTransfer);
		expect(result).toEqual([{ key: "value" }]);
	});

	it("should reject the promise if a file cannot be parsed", async () => {
		const mockFiles: File[] = [
			createMockFile("test.json", "application/json"),
		];

		class FileReaderMock {
			static EMPTY = 0;
			static LOADING = 1;
			static DONE = 2;
			readyState = FileReaderMock.EMPTY;
			result: string | null = null;
			error: DOMException | null = new DOMException(
				"Invalid JSON content"
			);

			onload: () => void = () => Promise.resolve(this.result);
			onerror: () => void = () => Promise.reject(this.error);

			readAsText() {
				setTimeout(() => {
					this.onerror();
				}, 0);
			}
		}

		global.FileReader = FileReaderMock as any;

		const dataTransfer: DataTransfer = createDataTransferMock(mockFiles);

		const promise = readJsonFilesFromDataTransfer(dataTransfer);

		await expect(promise).rejects.toThrow();
	});
});
