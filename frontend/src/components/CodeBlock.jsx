import React from 'react';

function CodeBlock({ code, language = 'python' }) {
  return (
    <div className="bg-gray-900 rounded-lg overflow-hidden">
      <pre className="p-4 overflow-x-auto">
        <code className="text-sm text-gray-100 font-mono">
          {code}
        </code>
      </pre>
    </div>
  );
}

export default CodeBlock;
