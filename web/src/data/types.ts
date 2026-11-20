export type Category = 'Boards' | 'Accessories' | 'Connectors' | 'Prototypes';
export type Validation = {
  cadValid: boolean;
  meshWatertight: boolean;
  slicerVerified: boolean;
  fitVerified: boolean;
  loadTested: boolean;
};
export type HookParams = {
  stemLengthIn: number;
  stemDiameterIn: number;
  lipDiameterIn: number;
};
export type StudioModel = {
  id: string;
  name: string;
  type: Category;
  tagline: string;
  description: string;
  interface: string;
  material: string;
  tags: string[];
  source: string;
  sourceUrl?: string;
  editable: string;
  accent: string;
  parameters?: HookParams;
  model: string;
  preview: string;
  downloads: Record<string, string>;
  boundsInches: number[];
  triangles: number;
  volumeCubicInches: number;
  validation: Validation;
  provenance: string;
};
export type StudioCatalog = {
  schemaVersion: string;
  generatedFrom: string;
  unit: 'in';
  verification: string;
  models: StudioModel[];
};
export const repoUrl = 'https://github.com/Danejw/opengrid-cad-library';
export const workflowUrl = `${repoUrl}/actions/workflows/build-cad.yml`;
export const assetUrl = (path: string) => `${import.meta.env.BASE_URL}assets/${path}`;
export const formatLength = (n: number) => `${n.toFixed(2)} in`;
