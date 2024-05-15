
$(document).ready(function () {
    $("#uf").change(function () {
        var uf = $(this).val();
        $.getJSON("/obter_cidades/", { uf: uf }, function (data) {
            $("#cidade").html(
                data.cidades
                    .map((cidade) => `<option value="${cidade}">${cidade}</option>`)
                    .join("")
            );
        });
    });
});
