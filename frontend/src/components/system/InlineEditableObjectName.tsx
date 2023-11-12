import { useAICStore } from '@/store/AICStore';
import { EditableObject, EditableObjectType } from '@/types/types';
import { cn } from '@/utils/styles';
import { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const InlineEditableObjectName = ({
  editableObject, // The editable object with 'id' and 'name'
  editableObjectType, // The type of the editable object
  isEditing,
  setIsEditing,
  className,
  isNew,
}: {
  editableObject: EditableObject;
  editableObjectType: EditableObjectType;
  isEditing: boolean;
  setIsEditing: (isEditing: boolean) => void;
  className?: string;
  isNew: boolean;
}) => {
  const [inputText, setInputText] = useState(editableObject.name);
  const inputRef = useRef<HTMLInputElement>(null);
  const location = useLocation();
  const navigate = useNavigate();

  const renameEditableObject = useAICStore((state) => state.renameEditableObject);

  useEffect(() => {
    if (isEditing) {
      setInputText(editableObject.name); // Reset input text to the current object name
      inputRef.current?.select(); // Select the text in the input
    }
  }, [isEditing, editableObject.name]);

  const handleRename = async () => {
    if (inputText.trim() && inputText !== editableObject.name) {
      const oldId = editableObject.id;
      const newId = await renameEditableObject(editableObject, inputText.trim(), isNew);

      //if we are in details of this object, we need to update the location
      if (location.pathname === `/${editableObjectType}s/${oldId}`) {
        navigate(`/${editableObjectType}s/${newId}`);
      }
    }
    setIsEditing(false); // Exit editing mode regardless of whether a change was made
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Escape') {
      setInputText(editableObject.name); // Reset the input text to the current object name
      setIsEditing(false); // Exit editing mode
    } else if (event.key === 'Enter') {
      handleRename(); // Commit the change
    }
  };

  return (
    <div onDoubleClick={() => setIsEditing(true)} className={cn('cursor-pointer', className)}>
      {isEditing ? (
        <input
          className="outline-none border h-[24px] border-gray-400 px-[5px] w-full text-white bg-gray-600 focus:border-primary resize-none overflow-hidden rounded-[4px] focus:outline-none"
          value={inputText}
          ref={inputRef}
          onBlur={handleRename} // Commit the change when the input loses focus
          onKeyDown={handleKeyDown} // Handle keyboard events
          onChange={(e) => setInputText(e.target.value)} // Update input text as the user types
        />
      ) : (
        <p className="leading-[18.2px] truncate">{editableObject.name}</p>
      )}
    </div>
  );
};

export default InlineEditableObjectName;
