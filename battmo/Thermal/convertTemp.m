%
% Function converting Chen struct to a struct that can do thermal
% simulation
%
function thermalStruct = convertTemp(Chen, Temp)
    fn=fieldnames(Temp)
    thermalStruct=Chen;
    for i=1:numel(fn)
        i
        if isstruct(Temp.(fn{i}))==0
            if isfield(Chen, fn{i}) ~=1
                thermalStruct.(fn{i})=Temp.(fn{i});
            end
        else
            if isfield(Chen, fn{i}) == 0
                thermalStruct.(fn{i})=Temp.(fn{i});
            else
                thermalStruct.(fn{i})=convertTemp(Chen.(fn{i}),Temp.(fn{i}));
            end
        end
    end
end
